#!/bin/bash
# Script para iniciar o backend da aplicação ChapaAmigo

# Definir variáveis de ambiente
export FLASK_APP=app.api
export FLASK_ENV=production
export PYTHONPATH=$HOME

BACKEND_DIR=$PWD

LOG_FILE=$HOME/logs/backend.log

mkdir -p $HOME/logs

cd $BACKEND_DIR

echo "$(date): Iniciando o servidor Flask em segundo plano..." >> $LOG_FILE
PID_FILE=$HOME/backend.pid

if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat $PID_FILE)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "$(date): Encerrando processo anterior (PID: $OLD_PID)..." >> $LOG_FILE
        kill -9 $OLD_PID
    fi
fi

nohup python3 -m app.api >> $LOG_FILE 2>&1 &
echo $! > $PID_FILE
echo "$(date): Servidor iniciado com PID $(cat $PID_FILE)" >> $LOG_FILE
