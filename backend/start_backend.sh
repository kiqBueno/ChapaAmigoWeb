#!/bin/bash
# Script para iniciar o backend da aplicação ChapaAmigo

# Definir variáveis de ambiente
export FLASK_APP=app.api
export FLASK_ENV=production
export PYTHONPATH=$HOME

# Usar diretório absoluto para garantir consistência
BACKEND_DIR=$HOME/domains/chapaamigo.com.br/backend
if [ ! -d "$BACKEND_DIR" ]; then
    # Fallback para o diretório atual se o caminho absoluto não existir
    BACKEND_DIR=$PWD
fi

LOG_FILE=$HOME/logs/backend.log
PID_FILE=$HOME/backend.pid

# Criar diretório de logs se não existir
mkdir -p $HOME/logs

# Mudar para o diretório do backend
cd $BACKEND_DIR

echo "$(date): Iniciando o servidor Flask em segundo plano..." >> $LOG_FILE
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat $PID_FILE)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "$(date): Encerrando processo anterior (PID: $OLD_PID)..." >> $LOG_FILE
        kill -9 $OLD_PID
    fi
    # Remover o arquivo PID para evitar conflitos
    rm -f $PID_FILE
fi

# Matar qualquer processo Python relacionado à API que possa estar rodando
pkill -f "python.*app.api" 2>/dev/null
sleep 2

# Usar disown para desvincular o processo do terminal
# O comando nohup já faz isso, mas vamos garantir com disown também
nohup python3 -m app.api >> $LOG_FILE 2>&1 &
PID=$!
echo $PID > $PID_FILE
disown $PID
echo "$(date): Servidor iniciado com PID $PID" >> $LOG_FILE
echo "$(date): O servidor está rodando em segundo plano e continuará mesmo após fechar o terminal" >> $LOG_FILE
