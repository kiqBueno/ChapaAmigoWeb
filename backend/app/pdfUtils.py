import os
import logging
import re
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from .imageUtils import cropImage, addTransparency
from .logging_config import setup_logging
import fitz
from PyPDF2 import PdfWriter

# Configure logging
setup_logging()

class PdfUtils:
    def __init__(self, data, outputPdf, images, useWatermark=True, photoPath=None, includeContract=False, includeDocuments=False, selectedGroups=None):
        self.data = data
        self.outputPdf = outputPdf
        self.images = images
        self.useWatermark = useWatermark
        self.photoPath = photoPath
        self.includeContract = includeContract
        self.includeDocuments = includeDocuments
        self.selectedGroups = self._process_selected_groups(selectedGroups)
        self.canvas = canvas.Canvas(outputPdf, pagesize=letter)
        self.width, self.height = letter
        self.y = self.height - 40
        self._register_fonts()

    def _process_selected_groups(self, selectedGroups):
        if not selectedGroups:
            return {}

        group_mappings = {
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

        processed_groups = {}
        for group_name, value in selectedGroups.items():
            if value and len(value) > 0:
                if group_name in group_mappings:
                    processed_groups[group_name] = group_mappings[group_name]
                else:
                    logging.warning(f"Group '{group_name}' does not have a mapping defined")

        return processed_groups

    def _register_fonts(self):
        pdfmetrics.registerFont(TTFont('Calibri', 'calibri.ttf'))
        pdfmetrics.registerFont(TTFont('Calibri-Bold', 'calibrib.ttf'))

    def save_specific_pages_as_images(self, pdfPath, pdfPassword):
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

    def _draw_text(self, x, y, text, font="Calibri", size=12, bold=False, max_width=None):
        self.canvas.setFont(f"{font}-Bold" if bold else font, size)
        max_width = max_width or (self.width - x - 40)  # Default max width is the page width minus margins
        words = text.split()
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            if self.canvas.stringWidth(test_line, f"{font}-Bold" if bold else font, size) > max_width:
                self.canvas.drawString(x, y, line)
                y -= size + 2  # Move to the next line
                line = word
            else:
                line = test_line
        if line:  # Draw the last line
            self.canvas.drawString(x, y, line)
        return y  # Return the updated y position

    def _add_watermark(self):
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

    def _add_photo(self):
        if not self.photoPath:
            logging.warning("No photo path provided.")
            return
        if not os.path.exists(self.photoPath):
            logging.error(f"Photo path does not exist: {self.photoPath}")
            return
        try:
            with open(self.photoPath, "rb") as img_file:
                img = ImageReader(img_file)
                self.canvas.drawImage(
                    img, x=self.width - 150, y=self.height - 200,
                    width=100, height=150, preserveAspectRatio=True, mask='auto'
                )
            logging.info("Photo added successfully.")
        except FileNotFoundError:
            logging.error(f"Photo file not found: {self.photoPath}")
        except Exception as e:
            logging.error(f"Failed to add photo: {e}")

    def _draw_group(self, title, keys):
        self.y -= 20
        self._draw_text(40, self.y, title)
        self.y -= 20
        for key in keys:
            if key in self.data:
                text = self.data[key]
                if key == "Total de Processos":
                    # Draw the summary of processes
                    self._ensure_space(20)
                    key_width = self.canvas.stringWidth(f"{key}: ", "Calibri-Bold", 12)
                    self._draw_text(60, self.y, f"{key}:", bold=True)
                    self.y = self._draw_text(60 + key_width + 10, self.y, str(text))
                    self.y -= 20
                    if int(text) == 0:
                        # Skip process details if total processes are zero
                        return
                elif isinstance(text, list) and key == "Número do Processo":
                    # Handle grouped processes
                    process_count = len(text)
                    for i in range(process_count):
                        self._ensure_space(20)
                        self._draw_text(60, self.y, f"Processo {i + 1}:", bold=True)
                        self.y -= 20
                        for process_key in ["Número do Processo", "Tipo", "Status", "Papel", "Valor da Causa", "Envolvidos", "Assunto", "Tribunal", "Data de Abertura", "Idade em Dias", "Data de Encerramento", "Última Atualização", "Última Movimentação"]:
                            if process_key in self.data and len(self.data[process_key]) > i:
                                value = self.data[process_key][i]
                                key_width = self.canvas.stringWidth(f"{process_key}: ", "Calibri-Bold", 12)
                                self._ensure_space(20)
                                self._draw_text(80, self.y, f"{process_key}:", bold=True)
                                self.y = self._draw_text(80 + key_width + 10, self.y, str(value) if value is not None else '-')
                                self.y -= 20
                        self.y -= 10
                    # Exit after processing all processes to avoid redundant drawing
                    return
                elif isinstance(text, list):
                    # Handle other lists
                    for item in text:
                        self._ensure_space(20)
                        key_width = self.canvas.stringWidth(f"{key}: ", "Calibri-Bold", 12)
                        self._draw_text(60, self.y, f"{key}:", bold=True)
                        self.y = self._draw_text(60 + key_width + 10, self.y, str(item) if item is not None else '-')
                        self.y -= 20
                else:
                    # Handle single values
                    text = str(text) if text is not None else '-'
                    key_width = self.canvas.stringWidth(f"{key}: ", "Calibri-Bold", 12)
                    self._ensure_space(20)
                    self._draw_text(60, self.y, f"{key}:", bold=True)
                    self.y = self._draw_text(60 + key_width + 10, self.y, text)
                    self.y -= 20
            else:
                key_width = self.canvas.stringWidth(f"{key}: ", "Calibri-Bold", 12)
                self._ensure_space(20)
                self._draw_text(60, self.y, f"{key}:", bold=True)
                self._draw_text(60 + key_width + 10, self.y, "-", font="Calibri")
                self.y -= 20
        self.y -= 20
        self.y = max(self.y, 40)

    def _ensure_space(self, required_space):
        if self.y - required_space < 40:
            self.canvas.showPage()
            self._add_watermark()
            self.canvas.setFont("Calibri", 12)
            self.y = self.height - 40

    def _add_confidentiality_contract(self):
        contract_path = os.path.join(os.path.dirname(__file__), 'Files', 'TERMO_FICHA_CADASTRO_PDF.pdf')
        if not os.path.exists(contract_path):
            return
        try:
            contract_doc = fitz.open(contract_path)
            for page_num in range(len(contract_doc)):
                if page_num > 0:
                    self.canvas.showPage()
                self._add_watermark()
                page = contract_doc.load_page(page_num)
                pix = page.get_pixmap(dpi=300)
                img_bytes = BytesIO(pix.tobytes())
                img = ImageReader(img_bytes)
                self.canvas.drawImage(img, 0, 0, width=self.width, height=self.height)
            contract_doc.close()
            self.canvas.showPage()
            self.y = self.height - 40
        except Exception:
            pass

    def create_pdf(self):
        content_added = False
        if self.includeContract:
            self._add_confidentiality_contract()
            content_added = True
        if self.photoPath:
            logging.info("Calling _add_photo to add the image.")
            self._add_photo()  # Ensure this is called before other content
            content_added = True
        for groupTitle, groupKeys in self.selectedGroups.items():
            if groupKeys:
                self._add_watermark()
                self._draw_group(groupTitle, groupKeys)
                content_added = True
        if self.includeDocuments and self.images:
            for imgBytes in self.images:
                if content_added:
                    self.canvas.showPage()
                self._add_watermark()
                croppedImgBytes = cropImage(imgBytes)
                img = ImageReader(croppedImgBytes)
                self.canvas.drawImage(img, 0, 0, width=self.width, height=self.height)
                content_added = True
        if content_added:
            self.canvas.save()
            self.outputPdf.seek(0)
