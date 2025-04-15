from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
from .processPdf import processPdf
from .extractPdfData import extractDataFromPdf
from .logging_config import setup_logging
import os
import json
import logging
from PyPDF2 import PdfWriter
from io import StringIO, BytesIO

setup_logging()

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
        return jsonify({"name": extracted_data.get("Nome", "Unknown")})
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

        output_pdf = processPdf(
            uploaded_pdf_path, password, useWatermark, includeContract,
            includeDocuments, selectedGroups, uploaded_image_path
        )

        # Encrypt the PDF in memory
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

@app.route('/get-logs')
def get_logs():
    return jsonify({"logs": log_capture_string.getvalue()})

if __name__ == '__main__':
    app.run(debug=True)