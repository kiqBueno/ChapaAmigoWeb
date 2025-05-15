#!/bin/bash
# Script para monitorar e reiniciar o backend se ele parar

# Definir variáveis
LOG_FILE=$HOME/logs/monitor.log
BACKEND_SCRIPT=$PWD/start_backend.sh
PID_FILE=$HOME/backend.pid

# Criar diretório de logs se não existir
mkdir -p $HOME/logs

# Função para iniciar o backend
start_backend() {
    echo "$(date): Iniciando o backend..." >> $LOG_FILE
    nohup bash $BACKEND_SCRIPT > /dev/null 2>&1 &
    echo $! > $PID_FILE
    echo "$(date): Backend iniciado com PID $(cat $PID_FILE)" >> $LOG_FILE
}

# Função para verificar se o backend está rodando
check_backend() {
    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null; then
            echo "$(date): Backend está rodando com PID $PID" >> $LOG_FILE
            return 0
        else
            echo "$(date): Backend com PID $PID não está mais rodando" >> $LOG_FILE
            return 1
        fi
    else
        echo "$(date): Arquivo PID não encontrado" >> $LOG_FILE
        return 1
    fi
}

# Verificar e iniciar/reiniciar o backend se necessário
if ! check_backend; then
    echo "$(date): Backend não está rodando, iniciando..." >> $LOG_FILE
    start_backend
else
    echo "$(date): Backend já está rodando" >> $LOG_FILE
fi
