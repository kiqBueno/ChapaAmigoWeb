import re
import logging
from PyPDF2 import PdfReader
from io import BytesIO
from ..utils.logging_config import setupLogging

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
                extracted_value = re.sub(r'(?<!\S) | (?!\S)', '', extracted_value)
            else:
                extracted_value = default
            logging.debug(f"Extracted value for key '{key}': {extracted_value}")
            data[key] = extracted_value

    fields = [
        (r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})", "Data e Hora", "--"),
        (r"Nome:\s*([A-Z\s]+)(?=\s*CPF|$)", "Nome", "--"),
        (r"Nascimento\s*(\d{2}/\d{2}/\d{4})", "Nascimento", "--"),
        (r"Idade\s*(\d+)", "Idade", "--"),
        (r"Sexo\s*([A-Za-z\-]+)(?=\s*Signo|$)", "Sexo", "--"),
        (r"RG\s*([\d\-]+|--|-)", "Rg", "--"),
        (r"CPF\s*([\d\.\-]+)", "Cpf", "--"),
        (r"DADOS DA CNH\s*CNH\s*([\w\-]*)", "CNH", "--"),
        (r"Nome da Mãe\s*([A-Z\s]+)", "Mãe", "--"),
        (r"Nome do Pai\s*([A-Z\s\-]+)(?=\s*CPF|$)", "Pai", "--"),
        (r"Óbito\?\s*(\w+)", "Óbito", "--"),
        (r"E-MAILS\s*Prioridade\s+E-mail(?:\s*\d+)?\s*([\w\.-]+@[\w\.-]+\.\w+)", "E-mails", "--", True),
    ]

    fields += [
        (r"Renda Mensal Presumida\s*R\$\s*([\d\.,]+)", "Renda Mensal Presumida", "--"),
    ]

    fields += [
        (r"Situação Cadastral\s*([A-Z]+)", "Situação Cadastral", "--"),
        (r"Inscrito em\s*(\d{2}/\d{2}/\d{4}|--|-)", "Inscrito em", "--"),
        (r"Última Consulta\s*(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2}|\d{2}/\d{2}/\d{4})", "Última Consulta", "--"),
        
    ]

    fields += [
        (r"DADOS DA CTPS\s*CTPS\s*([\w\-]*)", "CTPS", "--"),
        (r"Série\s*([\w\-]*)", "Série", "--"),
    ]

    fields += [
        (r"Título de Eleitor\s*([\w\-]*)", "Título de eleitor", "--"),
    ]

    fields += [
        (r"Passaporte\s*([\w\-]*)", "Passaporte", "--"),
        (r"País\s*(\w+|-)", "País", "--"),
        (r"Validade\s*(\d{2}/\d{2}/\d{4})", "Validade", "--"),
    ]

    fields += [
        (r"NIS \(PIS/PASEP\)\s*([\w\-]*)", "Nis (pis/pasep)", "--"),
        (r"NIS - Outros\s*([\w\-]*)", "Nis - outros", "--"),
        (r"CNS\s*([\d\-]+)", "Cns", "--"),
        (r"CNS - Outros\s*([\d\-]+)", "Cns - outros", "--"),
        (r"Inscrição Social\s*([\w\s\-]+)(?=\s*Relatório de Pessoa Física|$)", "Inscrição social", "--"),
    ]

    fields += [
        (r"Quantidade de Pagamentos\s*(\d+)", "Quantidade de Pagamentos", "--"),
        (r"Valor Total dos Pagamentos\s*R\$\s*([\d,.]+)", "Valor Total dos Pagamentos", "--"),
    ]

    fields += [
        (r"Valor total recebido como\s*beneficiario\s*R\$\s*([\d,.]+)", "Valor total recebido como beneficiário", "0"),
        (r"Valor total recebido como\s*responsável\s*R\$\s*([\d,.]+)", "Valor total recebido como responsável", "0"),
        (r"Valor total recebido como\s*benef./resp.\s*R\$\s*([\d,.]+)", "Valor total recebido como benef./resp.", "0"),
        (r"Primeira ocorrência\s*([a-z]{3}/\d{4})", "Primeira ocorrência", "--"),
        (r"Última ocorrência\s*([a-z]{3}/\d{4})", "Última ocorrência", "--"),
    ]

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
        (r"Assunto\s+([\s\S]+?)(?=\s+Tribunal\b|\s+Ano Abertura\b|\s+Status\b|\s+Papel\b|\s+Valor da Causa\b|\s+Envolvidos\b)", "Assunto", "--", True),
        (r"Tribunal\s+([^\n]+?(?=\s*(?:Data Abertura|Ano Abertura|$)))", "Tribunal", "--", True),
   
        (r"Papel\s*([A-Z\s]+)(?=\s*Valor)", "Papel", "--", True),
        (r"Valor da Causa\s*(?:R\$)?\s*([\d,.]+|--|-)", "Valor da Causa", "--", True),
        (r"Envolvidos\s*(\d+)", "Envolvidos", "--", True),
        (r"(?:Ano Abertura|Data Abertura)\s*(\d{4}|\d{2}/\d{2}/\d{2,4}|--|-)", "Ano de Abertura", "--", True),
        (r"Data Encerramento\s*((?:\d{2}/\d{2}/\d{2,4}|--|-)+)", "Data de Encerramento", "--", True),
        (r"Últ\. Atualização\s*(\d{2}/\d{2}/\d{2,4}|--|-)", "Última Atualização", "--", True),
        (r"Últ\. Movimentação\s*(\d{2}/\d{2}/\d{2,4}|--|-)", "Última Movimentação", "--", True),
    ]

    fields += [
        (r"Parentes - Disponíveis:\s*(\d+)", "Quantidade de Parentes", "--"),
        (r"(?:PARENTES|Parentes)[\s\S]*?(?:CPF[\s\S]*?Nome[\s\S]*?Tipo[\s\S]*?Idade[\s\S]*?Óbito[\s\S]*?(?:PEP|PPE)[\s\S]*?Renda[\s\S]*?)((?:(?:[\d\.\-]+|-)[\s\S]*?[A-Za-zÀ-ÖØ-öø-ÿ\s]+[\s\S]*?[A-Za-zÀ-ÖØ-öø-ÿ\(\)\s]+[\s\S]*?(?:\d+|-)+[\s\S]*?(?:[SN-])+[\s\S]*?(?:[SN-])+[\s\S]*?(?:R\$\s*[\d\.]+|-)+[\s\S]*?)(?:SOCIEDADES|Sociedades|$))", "Parentes Dados", "", True),
    ]

    fields += [
        (r"ENDEREÇOS\s*Prioridade\s*Tipo Endereço\s*Endereço Completo\s*((?:\s*\d+\s*-\s*[^\n]+)+)", "Endereços", [], True),
        (r"O relatório apresenta informações sobre o indivíduo.*?Este resumo foi gerado automaticamente.*?\.", "Resumo do Relatório", [], True),
    ] 
       
    for pattern, key, *default in fields:
        extract(pattern, key, *default)
    data["Parentes CPF"] = []
    data["Parentes Nome"] = []
    data["Parentes Tipo"] = []
    data["Parentes Idade"] = []
    data["Parentes Óbito"] = []
    data["Parentes PEP"] = []
    data["Parentes Renda"] = []
    
    if "Parentes Dados" in data and isinstance(data["Parentes Dados"], list) and data["Parentes Dados"][0] != "ERROR":
        raw_data = data["Parentes Dados"][0]
        
        parentes_pattern = r"((?:\d{3}\.){2}\d{3}-\d{2}|-)\s+([^\n]+?)\s+((?:MÃE|PAI|IRMÃO\s*\(Ã\)|AVÓ|TIO\s*\(A\)|PRIMO\s*\(A\)|SOBRINHO\s*\(A\))[^\n]*?)\s+(\d+|-)\s+([SN-])\s+([SN])\s+(R\$\s*[\d\.]+|-)"
        parentes_records = re.findall(parentes_pattern, raw_data)
        
        if not parentes_records:
            parentes_pattern_alt = r"(-)\s+([A-ZÀ-Ü\s]+?)\s+(MÃE|PAI|IRMÃO\s*\(Ã\)|AVÓ|TIO\s*\(A\)|PRIMO\s*\(A\)|SOBRINHO\s*\(A\)|[A-ZÀÂÁÔÖÕÍ]+)\s+(-)\s+(-)\s+([SN])\s+(-)"
            parentes_records = re.findall(parentes_pattern_alt, raw_data)
        
        if not parentes_records:
            complex_pattern = r"([A-ZÀ-Ü\s]+?)\s+(MÃE|PAI|IRMÃO\s*\(\s*Ã\s*\)|AVÓ|TIO\s*\(\s*A\s*\)|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\))\s+(\d+)\s+([SN])\s+([SN])\s+(R\$\s*[\d\.]+|-)"
            complex_matches = re.findall(complex_pattern, raw_data)
            
            for match in complex_matches:
                nome, tipo, idade, obito, pep, renda = match
                tipo = re.sub(r'\s+', '', tipo.replace(' (', '(').replace('( ', '(').replace(' )', ')'))
                parentes_records.append(("-", nome.strip(), tipo, idade, obito, pep, renda))
        
        if not parentes_records:
            lines = raw_data.strip().split('\n')
            parentes_records = []
            
            line_buffer = ""
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('CPF') or line == 'SOCIEDADES':
                    continue
                
                if line_buffer:
                    line_buffer += " " + line
                else:
                    line_buffer = line
                
                complete_pattern = r"^((?:\d{3}\.){2}\d{3}-\d{2}|-)\s+(.+?)\s+(MÃE|PAI|IRMÃO\s*\(\s*Ã\s*\)|AVÓ|TIO\s*\(\s*A\s*\)|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\))\s+(\d+|-)\s+([SN-])\s+([SN-])\s+(R\$\s*[\d\.]+|-)$"
                
                match = re.match(complete_pattern, line_buffer)
                if match:
                    cpf, nome, tipo, idade, obito, pep, renda = match.groups()
                    tipo = re.sub(r'\s+', '', tipo.replace(' (', '(').replace('( ', '(').replace(' )', ')'))
                    parentes_records.append((cpf.strip(), nome.strip(), tipo, idade, obito, pep, renda))
                    line_buffer = ""
                    continue
                
                if len(line_buffer.split()) > 20:
                    first_line = line_buffer.split()[0:10]
                    first_line_text = " ".join(first_line)
                    
                    old_match = re.match(r"((?:\d{3}\.){2}\d{3}-\d{2}|-)\s+(.+)", first_line_text)
                    if old_match:
                        cpf = old_match.group(1)
                        rest = old_match.group(2).strip()
                        
                        renda_match = re.search(r'\s+(R\$\s*[\d\.]+|-)$', rest)
                        if renda_match:
                            renda = renda_match.group(1)
                            rest = rest[:renda_match.start()].strip()
                        else:
                            renda = "-"
                        
                        pep_match = re.search(r'\s+([SN])$', rest)
                        if pep_match:
                            pep = pep_match.group(1)
                            rest = rest[:pep_match.start()].strip()
                        else:
                            pep = "-"
                        
                        obito_match = re.search(r'\s+([SN-])$', rest)
                        if obito_match:
                            obito = obito_match.group(1)
                            rest = rest[:obito_match.start()].strip()
                        else:
                            obito = "-"
                        
                        idade_match = re.search(r'\s+(\d+|-)$', rest)
                        if idade_match:
                            idade = idade_match.group(1)
                            rest = rest[:idade_match.start()].strip()
                        else:
                            idade = "-"
                        
                        tipo_match = re.search(r'\s+(MÃE|PAI|IRMÃO\s*\(\s*Ã\s*\)|AVÓ|TIO\s*\(\s*A\s*\)|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\))$', rest)
                        if tipo_match:
                            tipo = tipo_match.group(1)
                            tipo = re.sub(r'\s+', '', tipo.replace(' (', '(').replace('( ', '(').replace(' )', ')'))
                            nome = rest[:tipo_match.start()].strip()
                        else:
                            nome = rest
                            tipo = "-"
                        
                        parentes_records.append((cpf, nome, tipo, idade, obito, pep, renda))
                    
                    line_buffer = ""
        
        cpfs = []
        nomes = []
        tipos = []
        idades = []
        obitos = []
        peps = []
        rendas = []
        
        for record in parentes_records:
            cpf = record[0].strip()
            nome = record[1].strip()
            tipo = record[2].strip()
            idade = record[3].strip()
            obito = record[4].strip()
            pep = record[5].strip()
            renda = record[6].strip()
            
            nome_limpo = nome
        
            cpf_pattern = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
            cpf_match = re.search(cpf_pattern, nome)
            if cpf_match:
                nome_limpo = nome[:cpf_match.start()].strip()
            
            padrao_extra = r'\s+(IRMÃO\s*\(\s*Ã\s*\)|MÃE|PAI|AVÓ|TIO\s*\(\s*A\s*\)|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\))\s+\d+\s+[SN]\s+[SN]\s+R\$\s*[\d\.]+.*$'
            nome_limpo = re.sub(padrao_extra, '', nome_limpo).strip()
            
            nome_limpo = re.sub(r'\s+\d+\s*$', '', nome_limpo).strip()
            nome_limpo = re.sub(r'\s+R\$\s*[\d\.]+.*$', '', nome_limpo).strip()
            nome_limpo = re.sub(r'\s+[SN]\s*$', '', nome_limpo).strip()
            
            if len(nome_limpo) < 3:
                nome_limpo = nome 
                
            cpfs.append(cpf)
            nomes.append(nome_limpo)
            tipos.append(tipo)
            idades.append(idade)
            obitos.append(obito)
            peps.append(pep)
            rendas.append(renda)
        
        data["Parentes CPF"] = cpfs
        data["Parentes Nome"] = nomes
        data["Parentes Tipo"] = tipos
        data["Parentes Idade"] = idades
        data["Parentes Óbito"] = obitos
        data["Parentes PEP"] = peps
        data["Parentes Renda"] = rendas

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

    if "Ano de Abertura" in data and isinstance(data["Ano de Abertura"], list):
        processed_years = []
        for value in data["Ano de Abertura"]:
            if value in ["--", "-"]:
                processed_years.append("--")
            elif re.match(r"\d{2}/\d{2}/\d{2}", value): 
                year = "20" + value.split("/")[-1]
                processed_years.append(year)
            elif re.match(r"\d{2}/\d{2}/\d{4}", value):
                year = value.split("/")[-1]
                processed_years.append(year)
            else:
                processed_years.append(value)
        data["Ano de Abertura"] = processed_years

    data["Número"] = extractor.extract_multiple(r"\(\d{2}\) \d{4,5}-\d{4}", "Número", "--")

    logging.info("Data extracted successfully")
    return data