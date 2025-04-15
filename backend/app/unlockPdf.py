import logging
from .logging_config import setupLogging

setupLogging()

from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def unlockPdf(inputPdf, password='515608'):
    logging.info(f"Unlocking PDF: {inputPdf}")
    try:
        reader = PdfReader(inputPdf)
        reader.decrypt(password)

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        outputPdf = BytesIO()
        writer.write(outputPdf)
        outputPdf.seek(0)
        logging.info("PDF unlocked successfully")
        return outputPdf
    except Exception as e:
        logging.error(f"Failed to unlock PDF: {e}")
        raise