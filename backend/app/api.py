from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from .processPdf import processPdf, cropPdf
from .extractPdfData import extractDataFromPdf
from .logging_config import setupLogging
from .config import BASE_URL
import os
import json
import logging
from PyPDF2 import PdfWriter
from io import StringIO, BytesIO

setupLogging()

app = Flask(__name__)
CORS(app)

log_capture_string = StringIO()
log_handler = logging.StreamHandler(log_capture_string)
log_handler.setLevel(logging.WARNING)
logging.getLogger().addHandler(log_handler)

uploaded_pdf_path = None
uploaded_image_path = None

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    global uploaded_pdf_path
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file provided."}), 400

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

        output_pdf = processPdf(
            file=uploaded_pdf_path,
            password=password,
            useWatermark=useWatermark,
            includeContract=includeContract,
            includeDocuments=includeDocuments,
            selectedGroups=selectedGroups,
            photoPath=uploaded_image_path,
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
            from .unlockPdf import unlockPdf
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

@app.route('/get-logs')
def get_logs():
    return jsonify({"logs": log_capture_string.getvalue()})

if __name__ == '__main__':
    app.run(debug=True)