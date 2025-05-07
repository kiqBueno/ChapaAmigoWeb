import re
import logging
from PyPDF2 import PdfReader
from io import BytesIO
from .logging_config import setupLogging

setupLogging()

class MultiFieldExtractor:
    def __init__(self, text):
        self.text = text

    def extract_multiple(self, pattern, key, default="ERROR"):
        matches = re.findall(pattern, self.text, re.DOTALL)
        if matches:
            cleaned_matches = [
                re.sub(r'\s+', ' ', match.replace('\n', ' ')).strip()
                for match in matches
            ]
            normalized_matches = [
                re.sub(r'^\s+|\s+$', '', match)
                for match in cleaned_matches
            ]
            return normalized_matches
        return [default]

def normalize_text(text):
    if isinstance(text, list):
        return [re.sub(r'[^\S\r\n]+', ' ', re.sub(r'\s+', ' ', t)).replace('\n', ' ').strip() for t in text]
    return re.sub(r'[^\S\r\n]+', ' ', re.sub(r'\s+', ' ', text)).replace('\n', ' ').strip()

def extractDataFromPdf(filePath, password='515608'):
    logging.info(f"Extracting data from file: {filePath}")
    data = {}
    if isinstance(filePath, BytesIO):
        file = filePath
    else:
        file = open(filePath, 'rb')

    with file:
        reader = PdfReader(file)
        if reader.is_encrypted:
            reader.decrypt(password)
        text = "".join(page.extract_text() for page in reader.pages)

    extractor = MultiFieldExtractor(text)

    def extract(pattern, key, default="ERROR", multiple=False):
        if multiple:
            extracted_values = extractor.extract_multiple(pattern, key, default)
            logging.debug(f"Extracted values for key '{key}': {extracted_values}")
            data[key] = extracted_values
        else:
            match = re.search(pattern, text)
            if match:
                extracted_value = re.sub(r'\s+', ' ', match.group(1).replace('\n', ' ')).strip()
                extracted_value = re.sub(r'(?<!\S) | (?!\S)', '', extracted_value)  # Remove espaços extras
            else:
                extracted_value = default
            logging.debug(f"Extracted value for key '{key}': {extracted_value}")
            data[key] = extracted_value

    # Group: Basic Information
    fields = [
        (r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})", "Data e Hora", "--"),
        (r"Nome:\s*([A-Z\s]+)(?=\s*CPF|$)", "Nome", "--"),
        (r"Nascimento\s*(\d{2}/\d{2}/\d{4})", "Nascimento", "--"),
        (r"Idade\s*(\d+)", "Idade", "--"),
        (r"Sexo\s*([A-Za-z\-]+)(?=\s*Signo|$)", "Sexo", "--"),
        (r"RG\s*([\d]+)", "Rg", "--"),
        (r"CPF\s*([\d\.\-]+)", "Cpf", "--"),
        (r"DADOS DA CNH\s*CNH\s*([\w\-]*)", "CNH", "--"),
        (r"Nome da Mãe\s*([A-Z\s]+)", "Mãe", "--"),
        (r"Nome do Pai\s*([A-Z\s\-]+)(?=\s*CPF|$)", "Pai", "--"),
        (r"Óbito\?\s*(\w+)", "Óbito", "--"),
        (r"E-MAILS\s*Prioridade\s+E-mail(?:\s*\d+)?\s*([\w\.-]+@[\w\.-]+\.\w+)", "E-mails", "--", True),
    ]

    # Group: Financial Information
    fields += [
        (r"Renda Mensal Presumida\s*R\$\s*([\d\.,]+)", "Renda Mensal Presumida", "--"),
    ]

    # Group: Federal Revenue History
    fields += [
        (r"Situação Cadastral\s*([A-Z]+)", "Situação Cadastral", "--"),
        (r"Inscrito em\s*(\d{2}/\d{2}/\d{4}|--)", "Inscrito em", "--"),
        (r"Última Consulta\s*(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2}|\d{2}/\d{2}/\d{4})", "Última Consulta", "--"),
        
    ]

    # Group: CTPS Data
    fields += [
        (r"DADOS DA CTPS\s*CTPS\s*([\w\-]*)", "CTPS", "--"),
        (r"Série\s*([\w\-]*)", "Série", "--"),
    ]

    # Group: Electoral Title
    fields += [
        (r"Título de Eleitor\s*([\w\-]*)", "Título de eleitor", "--"),
    ]

    # Group: Passport Data
    fields += [
        (r"Passaporte\s*([\w\-]*)", "Passaporte", "--"),
        (r"País\s*(\w+|-)", "País", "--"),
        (r"Validade\s*(\d{2}/\d{2}/\d{4})", "Validade", "--"),
    ]

    # Group: Social Data
    fields += [
        (r"NIS \(PIS/PASEP\)\s*([\w\-]*)", "Nis (pis/pasep)", "--"),
        (r"NIS - Outros\s*([\w\-]*)", "Nis - outros", "--"),
        (r"CNS\s*([\d\-]+)", "Cns", "--"),
        (r"CNS - Outros\s*([\d\-]+)", "Cns - outros", "--"),
        (r"Inscrição Social\s*([\w\s\-]+)(?=\s*Relatório de Pessoa Física|$)", "Inscrição social", "--"),
    ]

    # Group: Payments
    fields += [
        (r"Quantidade de Pagamentos\s*(\d+)", "Quantidade de Pagamentos", "--"),
        (r"Valor Total dos Pagamentos\s*R\$\s*([\d,.]+)", "Valor Total dos Pagamentos", "--"),
    ]

    # Group: Emergency Aid
    fields += [
        (r"Valor total recebido como\s*beneficiario\s*R\$\s*([\d,.]+)", "Valor total recebido como beneficiário", "0"),
        (r"Valor total recebido como\s*responsável\s*R\$\s*([\d,.]+)", "Valor total recebido como responsável", "0"),
        (r"Valor total recebido como\s*benef./resp.\s*R\$\s*([\d,.]+)", "Valor total recebido como benef./resp.", "0"),
        (r"Primeira ocorrência\s*([a-z]{3}/\d{4})", "Primeira ocorrência", "--"),
        (r"Última ocorrência\s*([a-z]{3}/\d{4})", "Última ocorrência", "--"),
    ]

    # Group: Legal Processes
    fields += [
        (r"Total de Processos\s*(\d+)", "Total de Processos", "--"),
        (r"Como Requerente\s*(\d+)", "Como Requerente", "--"),
        (r"Como Requerido\s*(\d+)", "Como Requerido", "--"),
        (r"Como Outra Parte\s*(\d+)", "Como Outra Parte", "--"),
        (r"Nos Últimos 30 Dias\s*(\d+)", "Nos Últimos 30 Dias", "--"),
        (r"Nos Últimos 90 Dias\s*(\d+)", "Nos Últimos 90 Dias", "--"),
        (r"Nos Últimos 180 Dias\s*(\d+)", "Nos Últimos 180 Dias", "--"),
        (r"Nos Últimos 365 Dias\s*(\d+)", "Nos Últimos 365 Dias", "--"),
        (r"(\d{20}|(?:\d{7}-\d{2}\.\d{4}\.\d{1,2}\.\d{2}\.\d{4}))", "Número do Processo", "--", True),
        (r"Tipo\s*([A-Z\s]+)(?=\s*Status)", "Tipo", "--", True),
        (r"Status\s+([\w\s\-]+?)(?=\s+Papel|\s+Valor da Causa|\s+Envolvidos)", "Status", "--", True),
        (r"Assunto\s+([\s\S]+?)(?=\s+Tribunal\b|\s+Ano Abertura\b|\s+Status\b|\s+Papel\b|\s+Valor da Causa\b|\s+Envolvidos\b)", "Assunto", "--", True),  # Ajustado para capturar até antes de "Tribunal" ou outros delimitadores
        
        (r"Tribunal\s+([^\n]+?(?=\s*(?:Data Abertura|Ano Abertura|$)))", "Tribunal", "--", True),
   
        (r"Papel\s*([A-Z\s]+)(?=\s*Valor)", "Papel", "--", True),
        (r"Valor da Causa\s*(?:R\$)?\s*([\d,.]+|--)", "Valor da Causa", "--", True),
        (r"Envolvidos\s*(\d+)", "Envolvidos", "--", True),
        (r"(?:Ano Abertura|Data Abertura)\s*(\d{4}|\d{2}/\d{2}/\d{2}|--)", "Ano de Abertura", "--", True),
        (r"Data Encerramento\s*((?:\d{2}/\d{2}/\d{2}|--)+)", "Data de Encerramento", "--", True),
        (r"Últ\. Atualização\s*(\d{2}/\d{2}/\d{2})", "Última Atualização", "--", True),
        (r"Últ\. Movimentação\s*(\d{2}/\d{2}/\d{2}|--)", "Última Movimentação", "--", True),
    ]

    # Group: Report Summary
    fields += [
        (r"ENDEREÇOS\s*Prioridade\s*Tipo Endereço\s*Endereço Completo\s*((?:\s*\d+\s*-\s*[^\n]+)+)", "Endereços", [], True),
        (r"O relatório apresenta informações sobre o indivíduo.*?Este resumo foi gerado automaticamente.*?\.", "Resumo do Relatório", [], True),
    ]

    for pattern, key, *default in fields:
        extract(pattern, key, *default)

    # Post-processing for "Assunto"
    if "Assunto" in data and isinstance(data["Assunto"], list):
        processed_assuntos = []
        for assunto in data["Assunto"]:
            if isinstance(assunto, str) and assunto != "--":
                try:
                    index = assunto.lower().index("tribunal")
                    processed_assunto = assunto[:index].strip()
                    processed_assuntos.append(processed_assunto if processed_assunto else "--")
                except ValueError:
                    processed_assuntos.append(assunto)
            else:
                processed_assuntos.append(assunto)
        data["Assunto"] = processed_assuntos

    # Post-processing for "Ano de Abertura"
    if "Ano de Abertura" in data and isinstance(data["Ano de Abertura"], list):
        processed_years = []
        for value in data["Ano de Abertura"]:
            if re.match(r"\d{2}/\d{2}/\d{2}", value): 
                year = "20" + value.split("/")[-1]
                processed_years.append(year)
            else:
                processed_years.append(value)
        data["Ano de Abertura"] = processed_years

    # "Número" (phone)
    data["Número"] = extractor.extract_multiple(r"\(\d{2}\) \d{4,5}-\d{4}", "Número", "--")

    logging.info("Data extracted successfully")
    return data