#!/bin/bash
# Script para verificar o status do backend de forma detalhada

PID_FILE=$HOME/backend.pid
LOG_FILE=$HOME/logs/backend.log

echo "================================================"
echo "    VERIFICAÇÃO DE STATUS DO SERVIDOR BACKEND   "
echo "================================================"
echo ""

# Verificar se o arquivo de PID existe
if [ -f "$PID_FILE" ]; then
    PID=$(cat $PID_FILE)
    if ps -p $PID > /dev/null; then
        echo "✅ Backend está RODANDO com PID $PID"
        echo "   Processo: $(ps -p $PID -o cmd=)"
        echo "   Iniciado em: $(ps -p $PID -o lstart=)"
        echo "   Tempo de execução: $(ps -p $PID -o etime=)"
        echo "   Uso de CPU: $(ps -p $PID -o %cpu=)%"
        echo "   Uso de memória: $(ps -p $PID -o %mem=)%"
        echo ""
        echo "Últimas 10 linhas do log:"
        echo "----------------------------"
        if [ -f "$LOG_FILE" ]; then
            tail -n 10 $LOG_FILE
        else
            echo "❌ Arquivo de log não encontrado em $LOG_FILE"
        fi
    else
        echo "❌ Backend NÃO está rodando, mas arquivo PID existe (PID: $PID)"
        echo "   Este processo não está mais ativo."
        echo ""
        echo "   Para reiniciar o servidor, execute:"
        echo "   $ bash $HOME/domains/chapaamigo.com.br/backend/restart_backend.sh"
    fi
else
    # Verificar se o processo está rodando mesmo sem arquivo PID
    if pgrep -f "python.*app.api" > /dev/null; then
        REAL_PID=$(pgrep -f "python.*app.api" | head -1)
        echo "⚠️ Backend está rodando com PID $REAL_PID, mas o arquivo PID não existe"
        echo "   Recriando arquivo PID..."
        echo $REAL_PID > $PID_FILE
        echo "✅ Arquivo PID criado: $PID_FILE"
        echo ""
        echo "   Processo: $(ps -p $REAL_PID -o cmd=)"
        echo "   Iniciado em: $(ps -p $REAL_PID -o lstart=)"
    else
        echo "❌ Backend NÃO está rodando"
        echo ""
        echo "   Para iniciar o servidor, execute:"
        echo "   $ bash $HOME/domains/chapaamigo.com.br/backend/start_backend.sh"
    fi
fi

# Verificar se o cron está configurado corretamente
echo ""
echo "================================================"
echo "    VERIFICAÇÃO DE CONFIGURAÇÃO DO CRONTAB      "
echo "================================================"

if crontab -l 2>/dev/null | grep -q "monitor_backend.sh"; then
    echo "✅ Crontab está configurado para monitorar o backend"
    echo "   Configuração atual:"
    crontab -l | grep "monitor_backend.sh" | sed 's/^/   /'
else
    echo "❌ Crontab NÃO está configurado para monitorar o backend"
    echo "   Execute o hostinger_setup.sh para configurá-lo"
fi

echo ""
echo "================================================"do backend de forma detalhada

PID_FILE=$HOME/backend.pid
LOG_FILE=$HOME/logs/backend.log

echo "================================================"
echo "    VERIFICAÇÃO DE STATUS DO SERVIDOR BACKEND   "
echo "================================================"
echo ""

# Verificar se o arquivo de PID existe
if [ -f "$PID_FILE" ]; then
    PID=$(cat $PID_FILE)
    if ps -p $PID > /dev/null; then
        echo "✅ Backend está RODANDO com PID $PID"
        echo "   Processo: $(ps -p $PID -o cmd=)"
        echo "   Iniciado em: $(ps -p $PID -o lstart=)"
        echo "   Tempo de execução: $(ps -p $PID -o etime=)"
        echo "   Uso de CPU: $(ps -p $PID -o %cpu=)%"
        echo "   Uso de memória: $(ps -p $PID -o %mem=)%"
        echo ""
        echo "Últimas 10 linhas do log:"
        echo "----------------------------"
        if [ -f "$LOG_FILE" ]; then
            tail -n 10 $LOG_FILE
        else
            echo "❌ Arquivo de log não encontrado em $LOG_FILE"
        fi
    else
        echo "❌ Backend NÃO está rodando, mas arquivo PID existe (PID: $PID)"
        echo "   Este processo não está mais ativo."
    fi
else
    if pgrep -f "python3 -m app.api" > /dev/null; then
        REAL_PID=$(pgrep -f "python3 -m app.api")
        echo "⚠️ Backend está rodando com PID $REAL_PID, mas o arquivo PID não existe"
        echo "   Recreating PID file..."
        echo $REAL_PID > $PID_FILE
        echo "✅ PID file criado: $PID_FILE"
    else
        echo "❌ Backend NÃO está rodando"
        echo "   Execute o restart_backend.sh para iniciá-lo"
    fi
fi

echo ""
echo "Para verificar se as requisições estão funcionando:"
echo "curl -I http://localhost:8080/"
echo ""
echo "Para reiniciar o backend:"
echo "$HOME/domains/chapaamigo.com.br/backend/restart_backend.sh"
