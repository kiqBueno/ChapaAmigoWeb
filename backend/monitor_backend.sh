#!/bin/bash
# Script para monitorar e reiniciar o backend se ele parar

# Definir variáveis
LOG_FILE=$HOME/logs/monitor.log
BACKEND_DIR=$HOME/domains/chapaamigo.com.br/backend
BACKEND_SCRIPT=$BACKEND_DIR/start_backend.sh
PID_FILE=$HOME/backend.pid

# Criar diretório de logs se não existir
mkdir -p $HOME/logs

# Função para iniciar o backend
start_backend() {
    echo "$(date): Iniciando o backend..." >> $LOG_FILE
    cd $BACKEND_DIR
    nohup bash $BACKEND_SCRIPT > /dev/null 2>&1 &
    echo "$(date): Backend iniciado via script $BACKEND_SCRIPT" >> $LOG_FILE
}

# Função para verificar se o backend está rodando
check_backend() {
    # Verificar tanto pelo PID quanto pelo processo Python diretamente
    if [ -f $PID_FILE ] && pgrep -f "python.*app.api" > /dev/null; then
        PID=$(cat $PID_FILE)
        echo "$(date): Backend está rodando com PID $PID" >> $LOG_FILE
        return 0
    elif pgrep -f "python.*app.api" > /dev/null; then
        # Processo está rodando mas o PID_FILE está ausente ou incorreto
        PID=$(pgrep -f "python.*app.api" | head -1)
        echo "$(date): Backend está rodando com PID $PID (atualizado PID_FILE)" >> $LOG_FILE
        echo $PID > $PID_FILE
        return 0
    else
        echo "$(date): Backend não está rodando" >> $LOG_FILE
        return 1
    fi
}

# Verificar e iniciar/reiniciar o backend se necessário
if ! check_backend; then
    echo "$(date): Backend não está rodando, iniciando..." >> $LOG_FILE
    
    # Garantir que não há processos zumbis ou duplicados antes de reiniciar
    if [ -f $PID_FILE ]; then
        OLD_PID=$(cat $PID_FILE)
        if ps -p $OLD_PID > /dev/null 2>&1; then
            echo "$(date): Tentando encerrar processo anterior (PID: $OLD_PID)..." >> $LOG_FILE
            kill -9 $OLD_PID 2>/dev/null
            sleep 2
        fi
        rm -f $PID_FILE
    fi
    
    # Matar qualquer processo Python relacionado à API que possa estar travado
    pkill -f "python.*app.api" 2>/dev/null
    sleep 2
    
    # Iniciar o backend
    start_backend
else
    echo "$(date): Backend está rodando normalmente" >> $LOG_FILE
fi

# Se foi passado o argumento 'restart', forçar reinicialização
if [ "$1" = "restart" ]; then
    echo "$(date): Reiniciando backend por solicitação..." >> $LOG_FILE
    if [ -f $PID_FILE ]; then
        OLD_PID=$(cat $PID_FILE)
        kill -9 $OLD_PID 2>/dev/null
        rm -f $PID_FILE
    fi
    pkill -f "python.*app.api" 2>/dev/null
    sleep 2
    start_backend
fi
