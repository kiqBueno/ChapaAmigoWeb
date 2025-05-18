#!/bin/bash
# Script para ser executado através do painel de Cron Jobs da Hostinger

# Defina os caminhos absolutos para garantir consistência
BACKEND_DIR=/u279915365/domains/chapaamigo.com.br/backend
LOG_DIR=/u279915365/logs
PID_FILE=/u279915365/backend.pid

# Crie o diretório de logs se não existir
mkdir -p $LOG_DIR

# Escreva no log
echo "$(date): Script de painel da Hostinger iniciado" >> $LOG_DIR/cron_panel.log

# Verificar se o servidor está rodando
if pgrep -f "python.*app.api" > /dev/null; then
    echo "$(date): Servidor já está rodando" >> $LOG_DIR/cron_panel.log
    PID=$(pgrep -f "python.*app.api" | head -1)
    
    # Atualizar o arquivo PID se necessário
    if [ ! -f "$PID_FILE" ] || [ "$(cat $PID_FILE)" != "$PID" ]; then
        echo "$PID" > $PID_FILE
        echo "$(date): Arquivo PID atualizado para $PID" >> $LOG_DIR/cron_panel.log
    fi
else
    echo "$(date): Servidor não está rodando. Iniciando..." >> $LOG_DIR/cron_panel.log
    
    # Mudar para o diretório do backend e iniciar
    cd $BACKEND_DIR
    bash $BACKEND_DIR/start_backend.sh
    
    # Verificar se foi iniciado com sucesso
    sleep 3
    if pgrep -f "python.*app.api" > /dev/null; then
        echo "$(date): Servidor iniciado com sucesso" >> $LOG_DIR/cron_panel.log
    else
        echo "$(date): ERRO: Falha ao iniciar o servidor" >> $LOG_DIR/cron_panel.log
    fi
fi
