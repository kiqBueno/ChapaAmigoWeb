import os
import logging

def get_paths():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    is_production = '/domains/chapaamigo.com.br/' in current_dir or os.environ.get('PRODUCTION') == 'true'
    if is_production:
        # Em produção: app está em chapaamigo.com.br/backend/app/
        # current_dir = .../chapaamigo.com.br/backend/app/utils
        # backend_root = .../chapaamigo.com.br/backend
        # domain_root = .../chapaamigo.com.br
        backend_root = os.path.dirname(os.path.dirname(current_dir))  # backend/
        domain_root = os.path.dirname(backend_root)  # chapaamigo.com.br/
        
        paths = {
            'uploads_dir': backend_root,  # backend/ - onde ficam uploads/, batch_results/, etc
            'static_dir': os.path.join(backend_root, 'static'),
            'public_dir': os.path.join(domain_root, 'public_html'),
            'contract_paths': [
                os.path.join(backend_root, 'static', 'TERMO_FICHA_CADASTRO_PDF.pdf'),
                os.path.join(domain_root, 'public_html', 'TERMO_FICHA_CADASTRO_PDF.pdf'),
                '/u279915365/domains/chapaamigo.com.br/backend/static/TERMO_FICHA_CADASTRO_PDF.pdf',
                '/u279915365/domains/chapaamigo.com.br/public_html/TERMO_FICHA_CADASTRO_PDF.pdf'
            ]
        }
    else:
        # Em desenvolvimento: app está em backend/app/
        # current_dir = .../ChapaAmigoWeb/backend/app/utils
        # backend_root = .../ChapaAmigoWeb/backend
        # project_root = .../ChapaAmigoWeb
        backend_root = os.path.dirname(os.path.dirname(current_dir))  # backend/
        project_root = os.path.dirname(backend_root)  # ChapaAmigoWeb/
        
        paths = {
            'uploads_dir': backend_root,  # backend/ - onde ficam uploads/, batch_results/, etc
            'static_dir': os.path.join(backend_root, 'static'),
            'public_dir': os.path.join(project_root, 'public'),
            'contract_paths': [
                os.path.join(project_root, 'public', 'TERMO_FICHA_CADASTRO_PDF.pdf'),
                os.path.join(backend_root, 'static', 'TERMO_FICHA_CADASTRO_PDF.pdf')
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
    uploads_dir = os.path.join(paths['uploads_dir'], 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    return os.path.join(uploads_dir, filename)

def get_batch_results_path(filename):
    """Get the correct path for batch result files"""
    paths = get_paths()
    batch_results_dir = os.path.join(paths['uploads_dir'], 'batch_results')
    os.makedirs(batch_results_dir, exist_ok=True)
    return os.path.join(batch_results_dir, filename)

def get_batch_storage_path():
    """Get the correct path for batch storage directory"""
    paths = get_paths()
    batch_storage_dir = os.path.join(paths['uploads_dir'], 'batch_storage')
    os.makedirs(batch_storage_dir, exist_ok=True)
    return batch_storage_dir

def get_carousel_path():
    paths = get_paths()
    return paths['public_dir']
