import os
import logging
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from .imageUtils import cropImage, addTransparency
from .logging_config import setupLogging
import fitz
from PyPDF2 import PdfReader, PdfWriter

setupLogging()

class PdfUtils:
    def __init__(self, data, outputPdf, images, useWatermark=True, photoPath=None, includeContract=False, includeDocuments=False, selectedGroups=None):
        self.data = data
        self.outputPdf = outputPdf
        self.images = images
        self.useWatermark = useWatermark
        self.photoPath = photoPath
        self.includeContract = includeContract
        self.includeDocuments = includeDocuments
        self.selectedGroups = self._processSelectedGroups(selectedGroups)
        self.canvas = canvas.Canvas(outputPdf, pagesize=letter)
        self.width, self.height = letter
        self.y = self.height - 40
        self._registerFonts()

    def _processSelectedGroups(self, selectedGroups):
        if not selectedGroups:
            return {}

        groupMappings = {
            "CADASTROS BÁSICOS": [
                "Nome", "Nascimento", "Idade", "Sexo", "Rg", "Cpf", "Mãe", "Pai", "Óbito", "Endereços"
            ],
            "RENDA": [
                "Renda Mensal Presumida"
            ],
            "HISTÓRICO DA RECEITA FEDERAL": [
                "Situação Cadastral", "Inscrito em", "Última Consulta"
            ],
            "DADOS DA CTPS": [
                "CTPS", "Série"
            ],
            "TITULO ELEITORAL": [
                "Título de eleitor"
            ],
            "DADOS DO PASSAPORTE": [
                "Passaporte", "País", "Validade"
            ],
            "DADOS SOCIAIS": [
                "Nis (pis/pasep)", "Nis - outros", "Cns", "Cns - outros", "Inscrição social"
            ],
            "CELULARES E TELEFONES FIXO": [
                "Número"
            ],
            "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA": [
                "Quantidade de Pagamentos", "Valor Total dos Pagamentos"
            ],
            "AUXÍLIO EMERGENCIAL": [                
                "Valor total recebido como beneficiário", "Valor total recebido como responsável", 
                "Valor total recebido como benef./resp.", "Primeira ocorrência", "Última ocorrência"
            ],
            "PROCESSOS": [
                "Total de Processos", "Como Requerente", "Como Requerido", "Como Outra Parte",
                "Nos Últimos 30 Dias", "Nos Últimos 90 Dias", "Nos Últimos 180 Dias", "Nos Últimos 365 Dias",
                "Número do Processo", "Tipo", "Status", "Papel", "Valor da Causa", "Envolvidos", 
                "Assunto", "Tribunal", "Data de Abertura", "Idade em Dias", "Data de Encerramento", 
                "Última Atualização", "Última Movimentação"
            ],
        }

        processedGroups = {}
        for groupName, value in selectedGroups.items():
            if value and len(value) > 0:
                if groupName in groupMappings:
                    processedGroups[groupName] = groupMappings[groupName]
                else:
                    logging.warning(f"Group '{groupName}' does not have a mapping defined")

        return processedGroups

    def _registerFonts(self):
        pdfmetrics.registerFont(TTFont('Calibri', 'calibri.ttf'))
        pdfmetrics.registerFont(TTFont('Calibri-Bold', 'calibrib.ttf'))

    def saveSpecificPagesAsImages(self, pdfPath, pdfPassword):
        doc = fitz.open(pdfPath)
        if (doc.needs_pass):
            doc.authenticate(pdfPassword)
        keywords = ["Comprovante de Situação Cadastral no CPF", "Sistema Nacional de Informações Criminais", "Portal do BNMP"]
        images = []
        for pageNum in range(len(doc)):
            page = doc.load_page(pageNum)
            text = page.get_text()
            if any(keyword in text for keyword in keywords):
                pix = page.get_pixmap(dpi=300)
                imgBytes = BytesIO(pix.tobytes())
                images.append(imgBytes)
        return images

    def _drawText(self, x, y, text, font="Calibri", size=12, bold=False, maxWidth=None):
        self.canvas.setFont(f"{font}-Bold" if bold else font, size)
        maxWidth = maxWidth or (self.width - x - 40)
        words = text.split()
        line = ""
        for word in words:
            testLine = f"{line} {word}".strip()
            if self.canvas.stringWidth(testLine, f"{font}-Bold" if bold else font, size) > maxWidth:
                self.canvas.drawString(x, y, line)
                y -= size + 2
                line = word
            else:
                line = testLine
        if line:
            self.canvas.drawString(x, y, line)
        return y
    def _addWatermark(self):
        if not self.useWatermark:
            return
        logoPath = os.path.join(os.path.dirname(__file__), 'Files', 'LogoChapaAmigo.png')
        if not os.path.exists(logoPath):
            return
        try:
            self.canvas.saveState()
            self.canvas.translate(self.width / 2, self.height / 2)
            self.canvas.rotate(45)
            logoImgBytes = addTransparency(logoPath, 0.05)
            img = ImageReader(logoImgBytes)
            self.canvas.drawImage(img, -250, -125, width=500, height=250, mask='auto')
            self.canvas.restoreState()
        except Exception as e:
            logging.error(f"Failed to add watermark: {e}")

    def _addPhoto(self):
        if not self.photoPath:
            logging.warning("No photo path provided.")
            return
        if not os.path.exists(self.photoPath):
            logging.error(f"Photo path does not exist: {self.photoPath}")
            return
        try:
            with open(self.photoPath, "rb") as imgFile:
                img = ImageReader(imgFile)
                self.canvas.drawImage(
                    img, x=self.width - 150, y=self.height - 200,
                    width=100, height=150, preserveAspectRatio=True, mask='auto'
                )
            logging.info("Photo added successfully.")
        except FileNotFoundError:
            logging.error(f"Photo file not found: {self.photoPath}")
        except Exception as e:
            logging.error(f"Failed to add photo: {e}")

    def _drawGroup(self, title, keys):
        self.y -= 20
        self._drawText(40, self.y, title)
        self.y -= 20
        for key in keys:
            if key in self.data:
                text = self.data[key]
                if key == "Total de Processos":
                    self._ensureSpace(20)
                    keyWidth = self.canvas.stringWidth(f"{key}: ", "Calibri-Bold", 12)
                    self._drawText(60, self.y, f"{key}:", bold=True)
                    self.y = self._drawText(60 + keyWidth + 10, self.y, str(text))
                    self.y -= 20
                    if int(text) == 0:
                        return
                elif isinstance(text, list) and key == "Número do Processo":
                    processCount = len(text)
                    for i in range(processCount):
                        self._ensureSpace(20)
                        self._drawText(60, self.y, f"Processo {i + 1}:", bold=True)
                        self.y -= 20
                        for processKey in ["Número do Processo", "Tipo", "Status", "Papel", "Valor da Causa", "Envolvidos", "Assunto", "Tribunal", "Data de Abertura", "Idade em Dias", "Data de Encerramento", "Última Atualização", "Última Movimentação"]:
                            if processKey in self.data and len(self.data[processKey]) > i:
                                value = self.data[processKey][i]
                                keyWidth = self.canvas.stringWidth(f"{processKey}: ", "Calibri-Bold", 12)
                                self._ensureSpace(20)
                                self._drawText(80, self.y, f"{processKey}:", bold=True)
                                self.y = self._drawText(80 + keyWidth + 10, self.y, str(value) if value is not None else '-')
                                self.y -= 20
                        self.y -= 10
                    return
                elif isinstance(text, list):
                    for item in text:
                        self._ensureSpace(20)
                        keyWidth = self.canvas.stringWidth(f"{key}: ", "Calibri-Bold", 12)
                        self._drawText(60, self.y, f"{key}:", bold=True)
                        self.y = self._drawText(60 + keyWidth + 10, self.y, str(item) if item is not None else '-')
                        self.y -= 20
                else:
                    text = str(text) if text is not None else '-'
                    keyWidth = self.canvas.stringWidth(f"{key}: ", "Calibri-Bold", 12)
                    self._ensureSpace(20)
                    self._drawText(60, self.y, f"{key}:", bold=True)
                    self.y = self._drawText(60 + keyWidth + 10, self.y, text)
                    self.y -= 20
            else:
                keyWidth = self.canvas.stringWidth(f"{key}: ", "Calibri-Bold", 12)
                self._ensureSpace(20)
                self._drawText(60, self.y, f"{key}:", bold=True)
                self._drawText(60 + keyWidth + 10, self.y, "-", font="Calibri")
                self.y -= 20
        self.y -= 20
        self.y = max(self.y, 40)

    def _ensureSpace(self, requiredSpace):
        if self.y - requiredSpace < 40:
            self.canvas.showPage()
            self._addWatermark()
            self.canvas.setFont("Calibri", 12)
            self.y = self.height - 40

    def _addConfidentialityContract(self):
        contractPath = os.path.join(os.path.dirname(__file__), 'Files', 'TERMO_FICHA_CADASTRO_PDF.pdf')
        if not os.path.exists(contractPath):
            return
        try:
            contractDoc = fitz.open(contractPath)
            for pageNum in range(len(contractDoc)):
                if pageNum > 0:
                    self.canvas.showPage()
                self._addWatermark()
                page = contractDoc.load_page(pageNum)
                pix = page.get_pixmap(dpi=300)
                imgBytes = BytesIO(pix.tobytes())
                img = ImageReader(imgBytes)
                self.canvas.drawImage(img, 0, 0, width=self.width, height=self.height)
            contractDoc.close()
            self.canvas.showPage()
            self.y = self.height - 40
        except Exception:
            pass

    def createPdf(self):
        contentAdded = False
        if self.includeContract:
            self._addConfidentialityContract()
            contentAdded = True
        if self.photoPath:
            logging.info("Calling _add_photo to add the image.")
            self._addPhoto()
            contentAdded = True
        for groupTitle, groupKeys in self.selectedGroups.items():
            if groupKeys:
                self._addWatermark()
                self._drawGroup(groupTitle, groupKeys)
                contentAdded = True
        if self.includeDocuments and self.images:
            for imgBytes in self.images:
                if contentAdded:
                    self.canvas.showPage()
                self._addWatermark()
                croppedImgBytes = cropImage(imgBytes)
                img = ImageReader(croppedImgBytes)
                self.canvas.drawImage(img, 0, 0, width=self.width, height=self.height)
                contentAdded = True
        if contentAdded:
            self.canvas.save()
            self.outputPdf.seek(0)

    def cropPdf(self, inputPdfPath, outputPdfPath, cropTopRatio=0.085, cropBottomRatio=0.085):
        try:
            with open(inputPdfPath, 'rb') as inFile:
                reader = PdfReader(inFile)
                writer = PdfWriter()

                for page in reader.pages:
                    page_width = float(page.mediabox[2])
                    page_height = float(page.mediabox[3])

                    crop_top = page_height * cropTopRatio
                    crop_bottom = page_height * cropBottomRatio
                    page.mediabox.upper_right = (page_width, page_height - crop_top)
                    page.mediabox.lower_left = (0, crop_bottom)

                    writer.add_page(page)

                with open(outputPdfPath, 'wb') as outFile:
                    writer.write(outFile)

        except Exception as e:
            logging.error(f"Error cropping PDF: {e}")
            raise
