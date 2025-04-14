import os
import tempfile
import logging
from typing import Optional
from io import BytesIO
from .pdfUtils import PdfUtils
from .extractPdfData import extractDataFromPdf
from .unlockPdf import destravarPdf

def processPdf(
    file: str,
    password: str,
    useWatermark: bool,
    includeContract: bool,
    includeDocuments: bool,
    selectedGroups: dict,
    photoPath: Optional[str] = None,
) -> BytesIO:
    try:
        if not file:
            raise ValueError("Invalid file path provided.")

        decrypted_pdf = destravarPdf(file, password)
        logging.info("PDF successfully decrypted.")

        if photoPath and not os.path.exists(photoPath):
            raise FileNotFoundError(f"Photo path does not exist: {photoPath}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
            temp_pdf_file.write(decrypted_pdf.read())
            temp_pdf_path = temp_pdf_file.name

        extractedData = extractDataFromPdf(decrypted_pdf, password)
        images = PdfUtils(None, None, None).save_specific_pages_as_images(temp_pdf_path, password)
        selectedGroups = {group: keys for group, keys in selectedGroups.items() if isinstance(keys, list) and keys}

        outputPdf = BytesIO()
        pdfUtils = PdfUtils(
            extractedData, outputPdf, images, useWatermark, photoPath,
            includeContract, includeDocuments, selectedGroups
        )
        pdfUtils.create_pdf()

        os.remove(temp_pdf_path)
        return outputPdf

    except Exception as e:
        logging.error(f"Error in processPdf: {e}")
        raise