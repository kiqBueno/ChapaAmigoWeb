import os
import logging

def get_paths():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    is_production = '/domains/chapaamigo.com.br/' in current_dir or os.environ.get('PRODUCTION') == 'true'
    if is_production:
        base_domain_path = os.path.join(os.environ.get('HOME', ''), 'domains', 'chapaamigo.com.br')
        
        if not os.path.exists(base_domain_path):
            parts = current_dir.split(os.sep)
            for i, part in enumerate(parts):
                if 'chapaamigo.com.br' in part:
                    base_domain_path = os.sep.join(parts[:i+1])
                    break
        
        paths = {
            'uploads_dir': os.path.join(base_domain_path, 'backend', 'uploads'),
            'static_dir': os.path.join(base_domain_path, 'backend', 'static'),
            'public_dir': os.path.join(base_domain_path, 'public_html'),
            'contract_paths': [
                os.path.join(base_domain_path, 'backend', 'static', 'TERMO_FICHA_CADASTRO_PDF.pdf'),
                os.path.join(base_domain_path, 'public_html', 'TERMO_FICHA_CADASTRO_PDF.pdf'),
                '/u279915365/domains/chapaamigo.com.br/backend/static/TERMO_FICHA_CADASTRO_PDF.pdf',
                '/u279915365/domains/chapaamigo.com.br/public_html/TERMO_FICHA_CADASTRO_PDF.pdf'
            ]
        }
    else:
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        paths = {
            'uploads_dir': project_root,
            'static_dir': os.path.join(project_root, 'backend', 'static'),
            'public_dir': os.path.join(project_root, 'public'),
            'contract_paths': [
                os.path.join(project_root, 'public', 'TERMO_FICHA_CADASTRO_PDF.pdf'),
                os.path.join(project_root, 'backend', 'static', 'TERMO_FICHA_CADASTRO_PDF.pdf')
            ]
        }    
    for dir_key in ['uploads_dir', 'static_dir']:
        dir_path = paths[dir_key]
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"Diretório criado: {dir_path}")
            except Exception as e:
                logging.error(f"Erro ao criar diretório {dir_path}: {e}")
    
    if not os.path.exists(paths['public_dir']):
        try:
            os.makedirs(paths['public_dir'], exist_ok=True)
            logging.info(f"Diretório public criado: {paths['public_dir']}")
        except Exception as e:
            logging.warning(f"Não foi possível criar diretório public {paths['public_dir']}: {e}")
    
    logging.info(f"Ambiente detectado: {'Produção' if is_production else 'Desenvolvimento'}")
    logging.info(f"Caminhos configurados: {paths}")
    
    return paths

def get_contract_path():
    paths = get_paths()
    
    for contract_path in paths['contract_paths']:
        if os.path.exists(contract_path):
            logging.info(f"Contrato encontrado em: {contract_path}")
            return contract_path
    
    logging.error("Contrato não encontrado em nenhum dos caminhos possíveis")
    logging.error(f"Caminhos verificados: {paths['contract_paths']}")
    return None

def get_upload_path(filename):
    paths = get_paths()
    return os.path.join(paths['uploads_dir'], filename)

def get_carousel_path():
    paths = get_paths()
    return paths['public_dir']
