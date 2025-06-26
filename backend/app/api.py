from .processPdf import processPdf, cropPdf
from .extractPdfData import extractDataFromPdf
from .unlockPdf import unlockPdf
from .logging_config import setupLogging
from .path_config import get_upload_path, get_carousel_path
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
import os
import json
import logging
from PIL import Image
from PyPDF2 import PdfWriter
from io import BytesIO
from waitress import serve

setupLogging()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://chapaamigo.com.br", "http://localhost:5173"], "supports_credentials": True}})

@app.after_request
def after_request(response):
    if response.mimetype == 'application/json':
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
    
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

uploaded_pdf_path = None
uploaded_image_path = None

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    global uploaded_pdf_path, uploaded_image_path
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file provided."}), 400

        uploaded_image_path = None
        uploaded_pdf_path = get_upload_path('uploaded_pdf.pdf')
        file.save(uploaded_pdf_path)        
        extracted_data = extractDataFromPdf(uploaded_pdf_path)
        logging.debug(f"Extracted data: {extracted_data}")
        
        return Response(
            json.dumps({
                "name": extracted_data.get("Nome", "Unknown")
            }, ensure_ascii=False),
            content_type="application/json"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload-image', methods=['POST'])
def upload_image():
    global uploaded_image_path
    try:
        image = request.files.get('image')
        if not image:
            return jsonify({"error": "No image provided."}), 400

        uploaded_image_path = get_upload_path('uploaded_image.png')
        image.save(uploaded_image_path)
        return jsonify({"message": "Image uploaded successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    global uploaded_pdf_path, uploaded_image_path
    try:
        if not uploaded_pdf_path:
            return jsonify({"error": "No PDF uploaded."}), 400        
        password = request.form.get('password', '515608')
        useWatermark = request.form.get('useWatermark', 'true') == 'true'
        includeContract = request.form.get('includeContract', 'true') == 'true'
        includeDocuments = request.form.get('includeDocuments', 'true') == 'true'
        selectedGroups = json.loads(request.form.get('selectedGroups', '{}'))
        summaryTexts = json.loads(request.form.get('summaryTexts', '[]'))
        
        current_photo_path = None
        if uploaded_image_path and os.path.exists(uploaded_image_path):
            current_photo_path = uploaded_image_path
        
        output_pdf = processPdf(
            file=uploaded_pdf_path,
            password=password,
            useWatermark=useWatermark,
            includeContract=includeContract,
            includeDocuments=includeDocuments,
            selectedGroups=selectedGroups,
            photoPath=current_photo_path,
            summaryTexts=summaryTexts
        )

        encrypted_pdf = BytesIO()
        writer = PdfWriter()
        writer.append(output_pdf)
        writer.encrypt("1234")
        writer.write(encrypted_pdf)
        encrypted_pdf.seek(0)

        return send_file(
            encrypted_pdf,
            mimetype='application/pdf',
            as_attachment=True,
            download_name="Processed_Report.pdf"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/crop-pdf', methods=['POST'])
def crop_pdf():
    global uploaded_pdf_path
    try:
        if not uploaded_pdf_path or not os.path.exists(uploaded_pdf_path):
            logging.error("No PDF uploaded or file does not exist.")
            return jsonify({"error": "No PDF uploaded."}), 400

        logging.info(f"Cropping PDF: {uploaded_pdf_path}")
        
        try:
            with open(uploaded_pdf_path, 'rb') as f:
                unlocked_pdf = unlockPdf(f)
        except Exception as e:
            logging.error(f"Failed to unlock PDF: {e}")
            return jsonify({"error": "Failed to unlock PDF."}), 500

        cropped_pdf = cropPdf(unlocked_pdf)

        return send_file(
            cropped_pdf,
            mimetype='application/pdf',
            as_attachment=True,
            download_name="Cropped_PDF.pdf"
        )
    except Exception as e:
        logging.error(f"Error in crop_pdf endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/carousel-images', methods=['GET'])
def get_carousel_images():
    """Get list of carousel images with their status"""
    try:
        public_path = get_carousel_path()
        
        images = []
        carousel_config_path = os.path.join(public_path, 'carousel_config.json')
        
        if os.path.exists(carousel_config_path):
            with open(carousel_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {
                'images': [
                    {'id': i, 'filename': f'carrousel{i}.jpg', 'alt': f'Carrossel {i}', 'isActive': True}
                    for i in range(1, 7)                ]
            }
            with open(carousel_config_path, 'w', encoding='utf-8') as f:                
                json.dump(config, f, indent=2, ensure_ascii=False)
        
        # Validar e corrigir configuração
        config = validate_carousel_config(config)
        
        for img_config in config['images']:
            img_path = os.path.join(public_path, img_config['filename'])
            img_config['exists'] = os.path.exists(img_path)
        
        # Retornar com headers explícitos para garantir Content-Type correto
        return Response(
            json.dumps(config, ensure_ascii=False),
            content_type='application/json; charset=utf-8',
            headers={
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        )
    except Exception as e:
        logging.error(f"Error getting carousel images: {e}")
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            status=500,
            content_type='application/json; charset=utf-8'
        )

@app.route('/carousel-image/<filename>')
def serve_carousel_image(filename):
    """Serve carousel images from the configured public path"""
    try:
        public_path = get_carousel_path()
          # Validar que o arquivo é uma imagem do carrossel
        if not filename.startswith('carrousel') or not filename.endswith('.jpg'):
            return jsonify({"error": "Invalid filename"}), 400
        
        image_path = os.path.join(public_path, filename)
        
        if os.path.exists(image_path):
            response = send_file(image_path, mimetype='image/jpeg')
            response.headers['Cache-Control'] = 'public, max-age=300'  # Cache por 5 minutos
            return response
        else:
            # Retornar imagem placeholder se não existir
            placeholder_path = os.path.join(public_path, 'placeholder-image.svg')
            if os.path.exists(placeholder_path):
                response = send_file(placeholder_path, mimetype='image/svg+xml')
                response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache por 1 hora
                return response
            else:
                return jsonify({"error": "Image not found"}), 404
                
    except Exception as e:
        logging.error(f"Error serving carousel image {filename}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/upload-carousel-image', methods=['POST'])
def upload_carousel_image():
    """Upload a new carousel image"""
    try:
        image = request.files.get('image')
        image_id = request.form.get('imageId')
        
        if not image or not image_id:
            return jsonify({"error": "Image and imageId are required"}), 400
        
        try:
            image_id = int(image_id)
            if image_id < 1 or image_id > 12:
                return jsonify({"error": "ImageId must be between 1 and 12"}), 400
        except ValueError:
            return jsonify({"error": "Invalid imageId"}), 400
        
        public_path = get_carousel_path()
        if not os.path.exists(public_path):
            os.makedirs(public_path)
        
        try:
            image.stream.seek(0)  # Reset stream position
            img = Image.open(image.stream)
            img.verify()
        except Exception:
            return jsonify({"error": "Invalid image file"}), 400
        image.stream.seek(0)  # Reset again for actual use
        
        filename = f'carrousel{image_id}.jpg'
        image_path = os.path.join(public_path, filename)
        
        logging.info(f"Uploading image for ID {image_id}, filename: {filename}")
        
        img = Image.open(image.stream)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        max_size = (1920, 1080)
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            try:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            except AttributeError:
                img.thumbnail(max_size)
        
        img.save(image_path, 'JPEG', quality=85, optimize=True)
        
        carousel_config_path = os.path.join(public_path, 'carousel_config.json')
        config = {"images": []}
        if os.path.exists(carousel_config_path):
            with open(carousel_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        image_found = False
        for img_info in config['images']:
            if img_info['id'] == image_id:
                img_info['filename'] = filename
                img_info['isActive'] = True
                image_found = True
                break
        
        if not image_found:
            config['images'].append({
                'id': image_id,
                'filename': filename,
                'alt': f'Carrossel {image_id}',
                'isActive': True
            })
        
        config['images'].sort(key=lambda x: x['id'])
        
        # Aplicar validação final da configuração
        config = validate_carousel_config(config)
        
        with open(carousel_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return jsonify({"message": "Image uploaded successfully", "filename": filename})
    
    except Exception as e:
        logging.error(f"Error uploading carousel image: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/toggle-carousel-image', methods=['POST'])
def toggle_carousel_image():
    """Toggle active status of a carousel image"""
    try:
        data = request.get_json()
        image_id = data.get('imageId')
        is_active = data.get('isActive')
        if image_id is None or is_active is None:
            return jsonify({"error": "imageId and isActive are required"}), 400
        
        public_path = get_carousel_path()
        carousel_config_path = os.path.join(public_path, 'carousel_config.json')
        
        if not os.path.exists(carousel_config_path):
            return jsonify({"error": "Carousel configuration not found"}), 404
        
        with open(carousel_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        for img_info in config['images']:
            if img_info['id'] == image_id:
                img_info['isActive'] = is_active
                break
        
        with open(carousel_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return jsonify({"message": "Image status updated successfully"})
    
    except Exception as e:
        logging.error(f"Error toggling carousel image: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/reorder-carousel-images', methods=['POST'])
def reorder_carousel_images():
    """Reorder carousel images"""
    try:
        data = request.get_json()
        source_id = data.get('sourceId')
        target_id = data.get('targetId')
        if source_id is None or target_id is None:
            return jsonify({"error": "sourceId and targetId are required"}), 400
        
        public_path = get_carousel_path()
        carousel_config_path = os.path.join(public_path, 'carousel_config.json')
        
        if not os.path.exists(carousel_config_path):
            return jsonify({"error": "Carousel configuration not found"}), 404
        
        with open(carousel_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        source_img = None
        target_img = None
        source_index = -1
        target_index = -1
        
        for i, img in enumerate(config['images']):
            if img['id'] == source_id:
                source_img = img.copy()
                source_index = i
            elif img['id'] == target_id:
                target_img = img.copy()
                target_index = i
        
        if not source_img or not target_img or source_index == -1 or target_index == -1:
            return jsonify({"error": "Source or target image not found"}), 404
          # Troca apenas o conteúdo (filename, alt, isActive), mantendo os IDs nas posições
        source_filename = source_img['filename']
        source_alt = source_img['alt']
        source_isActive = source_img['isActive']
        
        target_filename = target_img['filename']
        target_alt = target_img['alt']
        target_isActive = target_img['isActive']
        
        # Atualiza o conteúdo, mantendo os IDs nas posições originais
        config['images'][source_index]['filename'] = target_filename
        config['images'][source_index]['alt'] = target_alt
        config['images'][source_index]['isActive'] = target_isActive
        
        config['images'][target_index]['filename'] = source_filename
        config['images'][target_index]['alt'] = source_alt
        config['images'][target_index]['isActive'] = source_isActive
          # Não precisamos mover arquivos físicos, pois os nomes dos arquivos 
        # são definidos pelo filename no config, não pelo ID da posição
        # Os arquivos físicos mantêm seus nomes originais
        logging.info(f"Reordering images: source_id={source_id}, target_id={target_id}")
        
        with open(carousel_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logging.info("Images reordered successfully")
        return jsonify({"message": "Images reordered successfully"})
    
    except Exception as e:
        logging.error(f"Error reordering carousel images: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete-carousel-image', methods=['POST'])
def delete_carousel_image():
    """Delete a carousel image"""
    try:
        data = request.get_json()
        image_id = data.get('imageId')
        
        if image_id is None:
            return jsonify({"error": "imageId is required"}), 400
        
        public_path = get_carousel_path()
        carousel_config_path = os.path.join(public_path, 'carousel_config.json')
        
        if not os.path.exists(carousel_config_path):
            return jsonify({"error": "Carousel configuration not found"}), 404
        
        image_filename = f"carrousel{image_id}.jpg"
        image_path = os.path.join(public_path, image_filename)
        
        if os.path.exists(image_path):
            os.remove(image_path)
        
        with open(carousel_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        for img_info in config['images']:
            if img_info['id'] == image_id:
                img_info['filename'] = ""
                img_info['isActive'] = False
                break
        
        with open(carousel_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return jsonify({"message": "Image deleted successfully"})
    
    except Exception as e:
        logging.error(f"Error deleting carousel image: {e}")
        return jsonify({"error": str(e)}), 500

def validate_carousel_config(config):
    """Validate and fix carousel configuration to avoid duplicated filenames"""
    seen_filenames = {}
    
    for img_info in config['images']:
        filename = img_info.get('filename', '')
        if filename and filename in seen_filenames:
            # Duplicated filename found, clear it from this entry
            logging.warning(f"Duplicate filename {filename} found in ID {img_info['id']}, clearing it")
            img_info['filename'] = ""
            img_info['isActive'] = False
        elif filename:
            seen_filenames[filename] = img_info['id']
    
    return config

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)