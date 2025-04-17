import os
import tempfile
import logging
from typing import Optional
from io import BytesIO
from .pdfUtils import PdfUtils
from .extractPdfData import extractDataFromPdf
from .unlockPdf import unlockPdf       
from PyPDF2 import PdfReader, PdfWriter


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

        decryptedPdf = unlockPdf(file, password)
        logging.info("PDF successfully decrypted.")

        if photoPath and not os.path.exists(photoPath):
            raise FileNotFoundError(f"Photo path does not exist: {photoPath}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tempPdfFile:
            tempPdfFile.write(decryptedPdf.read())
            tempPdfPath = tempPdfFile.name

        extractedData = extractDataFromPdf(decryptedPdf, password)
        images = PdfUtils(None, None, None).saveSpecificPagesAsImages(tempPdfPath, password)
        selectedGroups = {group: keys for group, keys in selectedGroups.items() if isinstance(keys, list) and keys}

        outputPdf = BytesIO()
        pdfUtils = PdfUtils(
            extractedData, outputPdf, images, useWatermark, photoPath,
            includeContract, includeDocuments, selectedGroups
        )
        pdfUtils.createPdf()

        os.remove(tempPdfPath)
        return outputPdf

    except Exception as e:
        logging.error(f"Error in processPdf: {e}")
        raise

def cropPdf(file: BytesIO) -> BytesIO:
    try:
        if not file:
            raise ValueError("Invalid file provided.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tempInputFile:
            tempInputFile.write(file.getvalue())
            tempInputPath = tempInputFile.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tempOutputFile:
            tempOutputPath = tempOutputFile.name

        pdfUtils = PdfUtils(None, None, None)
        pdfUtils.cropPdf(tempInputPath, tempOutputPath)

        reader = PdfReader(tempOutputPath)
        writer = PdfWriter()

        pages = reader.pages[1:-1] if len(reader.pages) > 2 else []
        for page in pages:
            writer.add_page(page)

        writer.encrypt("1234")

        outputPdf = BytesIO()
        writer.write(outputPdf)
        outputPdf.seek(0)

        os.remove(tempInputPath)
        os.remove(tempOutputPath)
        return outputPdf

    except Exception as e:
        logging.error(f"Error in cropPdf: {e}")
        raise