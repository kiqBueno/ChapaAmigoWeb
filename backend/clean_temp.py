#!/usr/bin/env python3

import sys
import os
import glob

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.path_config import get_paths, get_upload_path

def clean_temp_files():
    print("=== Limpeza de Arquivos Temporários ===\n")
    
    paths = get_paths()    
    uploads_dir = paths['uploads_dir']
    
    temp_patterns = [
        'uploaded_pdf.pdf',
        'uploaded_image.png',
        'temp_*.jpg',
        '*.tmp'
    ]
    
    cleaned_count = 0
    
    print("Procurando arquivos temporários em:", uploads_dir)
    
    for pattern in temp_patterns:
        root_files = glob.glob(os.path.join(os.path.dirname(uploads_dir), pattern))
        
        upload_files = glob.glob(os.path.join(uploads_dir, pattern))
        
        all_files = root_files + upload_files
        
        for file_path in all_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"   ✓ Removido: {file_path}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"   ✗ Erro ao remover {file_path}: {e}")
    
    if cleaned_count == 0:
        print("   Nenhum arquivo temporário encontrado.")
    else:
        print(f"\n✓ Limpeza concluída! {cleaned_count} arquivo(s) removido(s).")

if __name__ == "__main__":
    clean_temp_files()
