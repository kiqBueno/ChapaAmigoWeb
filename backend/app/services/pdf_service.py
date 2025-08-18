import os
import tempfile
import logging
from typing import Optional
from io import BytesIO
from ..utils.pdfUtils import PdfUtils
from .extract_service import extractDataFromPdf
from .unlock_service import unlockPdf       
from PyPDF2 import PdfReader, PdfWriter


def processPdf(
    file: str,
    password: str,
    useWatermark: bool,
    includeContract: bool,
    includeDocuments: bool,
    selectedGroups: dict,
    photoPath: Optional[str] = None,
    summaryTexts: Optional[list] = None,
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
        pdfUtils.summaryTexts = summaryTexts or extractedData.get("Resumo do Relatório", [])
        if isinstance(pdfUtils.summaryTexts, list) and any(isinstance(item, list) for item in pdfUtils.summaryTexts):
            pdfUtils.summaryTexts = [text for sublist in pdfUtils.summaryTexts for text in (sublist if isinstance(sublist, list) else [sublist])]
        pdfUtils.createPdf()

        os.remove(tempPdfPath)
        return outputPdf

    except Exception as e:
        logging.error(f"Error in processPdf: {e}")
        raise