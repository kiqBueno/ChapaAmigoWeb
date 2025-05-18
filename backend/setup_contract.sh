#!/bin/bash
# Script para configurar os arquivos de contrato

# Diretórios
BASE_DIR=$HOME/domains/chapaamigo.com.br
BACKEND_DIR=$BASE_DIR/backend
STATIC_DIR=$BACKEND_DIR/static
PUBLIC_DIR=$BASE_DIR/public

# Verificar se os diretórios existem
mkdir -p $STATIC_DIR

# Copiar arquivos de contrato para diretórios apropriados se existirem
echo "Copiando arquivos de contrato..."

# Copiar de public para static se existir
if [ -f "$PUBLIC_DIR/TERMO_FICHA_CADASTRO_PDF.pdf" ]; then
    cp "$PUBLIC_DIR/TERMO_FICHA_CADASTRO_PDF.pdf" "$STATIC_DIR/"
    echo "Arquivo TERMO_FICHA_CADASTRO_PDF.pdf copiado para $STATIC_DIR/"
fi

# Copiar de public para static se existir
if [ -f "$PUBLIC_DIR/Contrato-de-Adesao-aos-Termos-de-Uso-da-Plataforma-CHAPAAMIGO®.pdf" ]; then
    cp "$PUBLIC_DIR/Contrato-de-Adesao-aos-Termos-de-Uso-da-Plataforma-CHAPAAMIGO®.pdf" "$STATIC_DIR/"
    echo "Arquivo Contrato-de-Adesao-aos-Termos-de-Uso-da-Plataforma-CHAPAAMIGO®.pdf copiado para $STATIC_DIR/"
fi

echo "Configuração de arquivos de contrato concluída"
