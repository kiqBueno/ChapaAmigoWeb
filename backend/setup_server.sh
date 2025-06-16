#!/bin/bash
# Script de configuração inicial para o servidor

# Variáveis
# Ajustando caminhos para a estrutura da Hostinger
BASE_DIR=$HOME/domains/chapaamigo.com.br
BACKEND_DIR=$PWD
LOGS_DIR=$HOME/logs

# Criar diretórios necessários
echo "Criando diretórios necessários..."
mkdir -p $LOGS_DIR
mkdir -p "$BACKEND_DIR/uploads"
mkdir -p "$BASE_DIR/public"

# Instalar dependências Python
echo "Instalando dependências Python..."
# Verificar qual comando Python está disponível
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "Erro: Python não encontrado. Por favor, instale o Python antes de continuar."
    exit 1
fi

# Verificar se pip está disponível
if command -v pip3 >/dev/null 2>&1; then
    PIP_CMD="pip3"
elif command -v pip >/dev/null 2>&1; then
    PIP_CMD="pip"
else
    echo "Aviso: pip não encontrado. Tentando instalar dependências manualmente..."
    PIP_CMD="$PYTHON_CMD -m pip"
fi

# Tentar instalar dependências
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    echo "Instalando pacotes Python com: python3 -m pip install --user -r requirements.txt"
    python3 -m pip install --user -r "$BACKEND_DIR/requirements.txt"
else
    echo "Arquivo requirements.txt não encontrado em $BACKEND_DIR"
fi

# Configurar permissões
echo "Configurando permissões..."
chmod +x "$BACKEND_DIR/start_backend.sh" "$BACKEND_DIR/monitor_backend.sh"

# Verificar se o sistema usa systemd
if command -v systemctl >/dev/null 2>&1; then
    # Tentar configurar serviço systemd
    echo "Detectado systemd. Tentando configurar serviço..."
    if [ -d /etc/systemd/system ] && [ -w /etc/systemd/system ]; then
        sudo cp $BACKEND_DIR/chapaamigo.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable chapaamigo.service
        sudo systemctl start chapaamigo.service
        echo "Serviço systemd configurado e iniciado."
        
        echo "Configuração concluída! O backend está rodando como um serviço."
        echo "Para verificar o status: sudo systemctl status chapaamigo.service"
        echo "Para visualizar logs: sudo journalctl -u chapaamigo.service"
        exit 0
    else
        echo "Não foi possível instalar o serviço systemd. Continuando com configuração alternativa..."
    fi
fi

# Configurar cron para monitoramento (alternativa ao systemd)
echo "Verificando se temos acesso ao crontab..."
if command -v crontab >/dev/null 2>&1; then
    echo "Configurando cron para monitoramento..."
    if [ -f "$BACKEND_DIR/crontab.txt" ]; then
        (crontab -l 2>/dev/null || echo "") | grep -v "monitor_backend.sh" > /tmp/crontmp
        cat "$BACKEND_DIR/crontab.txt" >> /tmp/crontmp
        crontab /tmp/crontmp
        rm /tmp/crontmp
        echo "Cron configurado com sucesso."
    else
        echo "Arquivo crontab.txt não encontrado. Pulando configuração do cron."
    fi
else
    echo "Comando crontab não disponível. Você pode configurar um agendamento usando o painel de controle da Hostinger."
    echo "Configure um trabalho agendado para executar o seguinte comando a cada 5 minutos:"
    echo "bash $BACKEND_DIR/monitor_backend.sh"
fi

# Iniciar o backend
echo "Iniciando o backend..."
bash "$BACKEND_DIR/start_backend.sh"

echo "Configuração concluída! O backend deve estar rodando agora."
echo "Para verificar o status, use: ps aux | grep python3"
echo "Para verificar os logs: cat $LOGS_DIR/backend.log"
echo ""
echo "IMPORTANTE: Verifique se o frontend está configurado para acessar a API em:"
echo "dominio.com.br/api ou pelo IP e porta corretos."
