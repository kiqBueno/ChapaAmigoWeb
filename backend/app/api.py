from .processPdf import processPdf, cropPdf
from .extractPdfData import extractDataFromPdf
from .logging_config import setupLogging
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
import os
import json
import logging
import shutil
from PIL import Image
from PyPDF2 import PdfWriter
from io import BytesIO
from waitress import serve

setupLogging()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://chapaamigo.com.br", "http://localhost:5173"], "supports_credentials": True}})

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
        uploaded_pdf_path = os.path.join(os.getcwd(), 'uploaded_pdf.pdf')
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

        uploaded_image_path = os.path.join(os.getcwd(), 'uploaded_image.png')
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
            from app.unlockPdf import unlockPdf
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
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        public_path = os.path.join(project_root, 'public')
        
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
            with open(carousel_config_path, 'w', encoding='utf-8') as f:                json.dump(config, f, indent=2, ensure_ascii=False)
        
        for img_config in config['images']:
            img_path = os.path.join(public_path, img_config['filename'])
            img_config['exists'] = os.path.exists(img_path)
        
        return jsonify(config)
    except Exception as e:
        logging.error(f"Error getting carousel images: {e}")
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
        
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        public_path = os.path.join(project_root, 'public')
        if not os.path.exists(public_path):
            os.makedirs(public_path)
        
        try:
            img = Image.open(image)
            img.verify()
        except Exception:
            return jsonify({"error": "Invalid image file"}), 400
        
        image.seek(0)
        
        filename = f'carrousel{image_id}.jpg'
        image_path = os.path.join(public_path, filename)
        
        img = Image.open(image)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        max_size = (1920, 1080)
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
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
        
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        public_path = os.path.join(project_root, 'public')
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
        
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        public_path = os.path.join(project_root, 'public')
        carousel_config_path = os.path.join(public_path, 'carousel_config.json')
        
        if not os.path.exists(carousel_config_path):
            return jsonify({"error": "Carousel configuration not found"}), 404
        
        with open(carousel_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        source_img = None
        target_img = None
        
        for img in config['images']:
            if img['id'] == source_id:
                source_img = img.copy()
            elif img['id'] == target_id:
                target_img = img.copy()
        
        if not source_img or not target_img:            return jsonify({"error": "Source or target image not found"}), 404
        
        for img in config['images']:
            if img['id'] == source_id:
                img['filename'] = target_img['filename']
                img['alt'] = target_img['alt']
                img['isActive'] = target_img['isActive']
            elif img['id'] == target_id:
                img['filename'] = source_img['filename']
                img['alt'] = source_img['alt']
                img['isActive'] = source_img['isActive']
        
        source_file = os.path.join(public_path, f'carrousel{source_id}.jpg')
        target_file = os.path.join(public_path, f'carrousel{target_id}.jpg')
        temp_file = os.path.join(public_path, f'temp_carrousel.jpg')
        
        if os.path.exists(source_file) and os.path.exists(target_file):
            shutil.move(source_file, temp_file)
            shutil.move(target_file, source_file)
            shutil.move(temp_file, target_file)
        elif os.path.exists(source_file):
            shutil.move(source_file, target_file)
        elif os.path.exists(target_file):
            shutil.move(target_file, source_file)
        
        with open(carousel_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
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
        
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        public_path = os.path.join(project_root, 'public')
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

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)