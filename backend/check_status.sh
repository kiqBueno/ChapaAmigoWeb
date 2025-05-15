#!/bin/bash
# Script para verificar o status do backend

PID_FILE=$HOME/backend.pid

if [ -f "$PID_FILE" ]; then
    PID=$(cat $PID_FILE)
    if ps -p $PID > /dev/null; then
        echo "✅ Backend está RODANDO com PID $PID"
        echo "   Processo: $(ps -p $PID -o cmd=)"
        echo "   Iniciado em: $(ps -p $PID -o lstart=)"
        echo ""
        echo "Últimas 10 linhas do log:"
        echo "----------------------------"
        tail -n 10 $HOME/logs/backend.log
    else
        echo "❌ Backend NÃO está rodando, mas PID file existe (PID: $PID)"
        echo "   Execute o restart_backend.sh para reiniciá-lo"
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
