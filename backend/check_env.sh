#!/bin/bash
# Script para verificar o ambiente Python e suas dependências

echo "=== Verificação do Ambiente Python ==="
echo ""

# Verificar versão do Python
echo "Versão do Python:"
python3 --version
echo ""

# Verificar se conseguimos importar os módulos necessários
echo "Verificando módulos Python:"
python3 -c "import sys; print('Python path:', sys.path)"
echo ""

echo "Testando importações essenciais:"
MODULES=("flask" "flask_cors" "waitress" "reportlab" "fitz" "PyPDF2")
for module in "${MODULES[@]}"; do
    echo -n "Verificando $module... "
    if python3 -c "import $module" 2>/dev/null; then
        echo "OK"
    else
        echo "FALHA - Módulo não encontrado"
    fi
done

echo ""
echo "=== Verificação de Rede ==="
echo "Verificando conexão com localhost:8080:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 || echo "Falha ao conectar"
echo ""

echo "=== Verificação concluída ==="