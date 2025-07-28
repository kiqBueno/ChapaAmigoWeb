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
        (r"Tribunal\s+([A-Z0-9\s\-\/]+?)(?=\s*(?:Data Abertura|Ano Abertura|Relatório de Pessoa|\n|$))", "Tribunal", "--", True),
   
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
    
    logging.info(f"Parentes Dados exists: {'Parentes Dados' in data}")
    if "Parentes Dados" in data:
        logging.info(f"Parentes Dados type: {type(data['Parentes Dados'])}")
        logging.info(f"Parentes Dados content: {data['Parentes Dados']}")
    
    if "Parentes Dados" in data and isinstance(data["Parentes Dados"], list) and data["Parentes Dados"][0] != "ERROR":
        raw_data = data["Parentes Dados"][0]
        logging.info(f"Processing Parentes raw data: {raw_data[:200]}...")
        
        raw_data = raw_data.replace(' SOCIEDADES', '').strip()
        
        parentes_records = []
        
        parente_pattern = r'(\d{3}\.\d{3}\.\d{3}-\d{2})\s+([A-Z\s]+?)\s+(MÃE|PAI|IRMÃO\s*\(\s*Ã\s*\)|AVÓ|AVÔ|BISAVÓ|TIO\s*\(\s*A\s*\)|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\))\s+(\d+|\-)\s+([SN\-])\s+([SN\-])\s+(R\$\s*[\d\.]+|\-)'
        
        matches = re.findall(parente_pattern, raw_data)
        logging.info(f"Found {len(matches)} parente matches with CPF using improved pattern")
        
        for match in matches:
            cpf, nome, tipo, idade, obito, pep, renda = match
            nome_limpo = nome.strip()
            nome_limpo = re.sub(r'\s{2,}', ' ', nome_limpo)
            logging.info(f"Successfully parsed: {cpf} - {nome_limpo} - {tipo}")
            parentes_records.append((cpf.strip(), nome_limpo, tipo.strip(), idade.strip(), obito.strip(), pep.strip(), renda.strip()))
        
        alt_pattern = r'(\-)\s+([A-Z\s]+?)\s+(AVÔ|AVÓ|BISAVÓ|BISAVÔ|TIO\s*\(\s*A\s*\)|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\)|MÃE|PAI|IRMÃO\s*\(\s*Ã\s*\))\s+(\d+|\-)\s+(\-)\s+([SN\-])\s+(\-)'
        
        alt_matches = re.findall(alt_pattern, raw_data)
        logging.info(f"Found {len(alt_matches)} parente matches without CPF using alternative pattern")
        
        for match in alt_matches:
            cpf, nome, tipo, idade, obito, pep, renda = match
            nome_limpo = nome.strip()
            nome_limpo = re.sub(r'\s{2,}', ' ', nome_limpo)
            logging.info(f"Successfully parsed (no CPF): {cpf} - {nome_limpo} - {tipo}")
            parentes_records.append((cpf.strip(), nome_limpo, tipo.strip(), idade.strip(), obito.strip(), pep.strip(), renda.strip()))
        
        flexible_cpf_pattern = r'(\d{3}[\.\-]?\d{3}[\.\-]?\d{3}[\.\-]?\d{2})\s+([A-Z\s]+?)\s+(MÃE|PAI|IRMÃO\s*\(\s*Ã\s*\)|AVÓ|AVÔ|BISAVÓ|TIO\s*\(\s*A\s*\)|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\))\s+(\d+|\-)\s+([SN\-])\s+([SN\-])\s+(R\$\s*[\d\.]+|\-)'
        
        flexible_matches = re.findall(flexible_cpf_pattern, raw_data)
        logging.info(f"Found {len(flexible_matches)} parente matches with flexible CPF pattern")
        
        for match in flexible_matches:
            cpf, nome, tipo, idade, obito, pep, renda = match
            nome_limpo = nome.strip()
            nome_limpo = re.sub(r'\s{2,}', ' ', nome_limpo)
            
            if not any(rec[0] == cpf.strip() and rec[1] == nome_limpo for rec in parentes_records):
                logging.info(f"Successfully parsed (flexible CPF): {cpf} - {nome_limpo} - {tipo}")
                parentes_records.append((cpf.strip(), nome_limpo, tipo.strip(), idade.strip(), obito.strip(), pep.strip(), renda.strip()))
        
        multiline_name_pattern = r'(\d{3}\.\d{3}\.\d{3}-\d{2})\s+([A-Z\s]+?)(?:\n|\s+)([A-Z\s]+?)\s+(MÃE|PAI|IRMÃO\s*\(\s*Ã\s*\)|AVÓ|AVÔ|BISAVÓ|TIO\s*\(\s*A\s*\)|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\))\s+(\d+|\-)\s+([SN\-])\s+([SN\-])\s+(R\$\s*[\d\.]+|\-)'
        
        multiline_matches = re.findall(multiline_name_pattern, raw_data)
        logging.info(f"Found {len(multiline_matches)} parente matches with multiline names")
        
        for match in multiline_matches:
            cpf, nome_parte1, nome_parte2, tipo, idade, obito, pep, renda = match
            nome_completo = f"{nome_parte1.strip()} {nome_parte2.strip()}"
            nome_limpo = re.sub(r'\s{2,}', ' ', nome_completo).strip()
            
            if not any(rec[0] == cpf.strip() and rec[1] == nome_limpo for rec in parentes_records):
                logging.info(f"Successfully parsed (multiline name): {cpf} - {nome_limpo} - {tipo}")
                parentes_records.append((cpf.strip(), nome_limpo, tipo.strip(), idade.strip(), obito.strip(), pep.strip(), renda.strip()))
        
        no_cpf_pattern = r'(\-)\s+([A-Z\s]+?)\s+(AVÔ|AVÓ|BISAVÓ|BISAVÔ|TIO\s*\(\s*A\s*\)|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\)|MÃE|PAI|IRMÃO\s*\(\s*Ã\s*\))\s+(\d+|\-)\s+(\-)\s+([SN\-])\s+(\-)'
        
        no_cpf_matches = re.findall(no_cpf_pattern, raw_data)
        logging.info(f"Found {len(no_cpf_matches)} parente matches without CPF (enhanced pattern)")
        
        for match in no_cpf_matches:
            cpf, nome, tipo, idade, obito, pep, renda = match
            nome_limpo = nome.strip()
            nome_limpo = re.sub(r'\s{2,}', ' ', nome_limpo)
            
            if not any(rec[1] == nome_limpo and rec[2] == tipo.strip() for rec in parentes_records):
                logging.info(f"Successfully parsed (no CPF enhanced): {cpf} - {nome_limpo} - {tipo}")
                parentes_records.append((cpf.strip(), nome_limpo, tipo.strip(), idade.strip(), obito.strip(), pep.strip(), renda.strip()))
        
        special_cases = [
            r'(\d{3}\.\d{3}\.\d{3}-\d{2})\s+([A-Z\s]+?)\s+(TIO\s*\(\s*A\s*\))\s+(\d+\s+\d+)\s+([SN\-])\s+([SN\-])\s+(R\$\s*[\d\.]+|\-)',
            r'(\d{3}\.\d{3}\.\d{3}-\d{2})\s+([A-Z\s]+?)\s+(PRIM\s+O\s*\(\s*A\s*\))\s+(\d+|\-)\s+([SN\-])\s+([SN\-])\s+(R\$\s*[\d\.]+|\-)',
            r'(\d{3}\.\d{3}\.\d{3}-\d{2})\s+([A-Z\s]+?)(?:\s*\n\s*|\s{2,})([A-Z\s]*?)\s+(TIO\s*\(\s*A\s*\)|MÃE|PAI|IRMÃO\s*\(\s*Ã\s*\)|AVÓ|AVÔ|BISAVÓ|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\))\s+(\d+|\-)\s+([SN\-])\s+([SN\-])\s+(R\$\s*[\d\.]+|\-)'
        ]
        for pattern in special_cases:
            special_matches = re.findall(pattern, raw_data)
            logging.info(f"Found {len(special_matches)} special case matches")
            
            for match in special_matches:
                if len(match) == 7:
                    cpf, nome, tipo, idade, obito, pep, renda = match
                elif len(match) == 8:
                    cpf, nome_parte1, nome_parte2, tipo, idade, obito, pep, renda = match
                    nome = f"{nome_parte1.strip()} {nome_parte2.strip()}"
                else:
                    continue
                    
                nome_limpo = nome.strip()
                nome_limpo = re.sub(r'\s{2,}', ' ', nome_limpo)
                
                if "PRIM O" in tipo:
                    tipo = "PRIMO(A)"
                
                if " " in str(idade) and idade != "-":
                    idade = str(idade).split()[0]
                
                if not any(rec[0] == cpf.strip() and rec[1] == nome_limpo for rec in parentes_records):
                    logging.info(f"Successfully parsed (special): {cpf} - {nome_limpo} - {tipo}")
                    parentes_records.append((cpf.strip(), nome_limpo, tipo.strip(), str(idade).strip(), obito.strip(), pep.strip(), renda.strip()))
        
        logging.info(f"Total parentes records found: {len(parentes_records)}")
        
        for i, record in enumerate(parentes_records):
            logging.info(f"Registro {i+1}: {record}")
        
        cpfs = []
        nomes = []
        tipos = []
        idades = []
        obitos = []
        peps = []
        rendas = []
        
        for record in parentes_records:
            cpf, nome, tipo, idade, obito, pep, renda = record
            
            nome_limpo = nome
            
            cpf_pattern = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
            nome_limpo = re.sub(cpf_pattern, '', nome_limpo).strip()
            
            nome_limpo = re.sub(r'\s+(MÃE|PAI|IRMÃO\s*\(\s*Ã\s*\)|AVÓ|AVÔ|BISAVÓ|TIO\s*\(\s*A\s*\)|PRIMO\s*\(\s*A\s*\)|SOBRINHO\s*\(\s*A\s*\))\s+.*$', '', nome_limpo).strip()
            nome_limpo = re.sub(r'\s+\d+\s+[SN-]\s+[SN-]\s+.*$', '', nome_limpo).strip()
            
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
        
        logging.info(f"Final parentes data - CPFs: {len(cpfs)}, Nomes: {len(nomes)}, Total: {len(nomes)}")
        logging.info(f"Sample parentes data - Names: {nomes[:3] if nomes else 'None'}")

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