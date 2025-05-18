#!/bin/bash
# Script para verificar e reiniciar o backend

echo "Checking if backend is running..."
PID_FILE=$HOME/backend.pid

if [ -f "$PID_FILE" ] && pgrep -f "python3 -m app.api" > /dev/null; then
    PID=$(cat $PID_FILE)
    echo "Backend is already running with PID $PID. Restarting..."
    kill -9 $PID
    rm $PID_FILE
    sleep 2
else
    echo "Backend is not running or PID file is missing."
    if [ -f "$PID_FILE" ]; then
        rm $PID_FILE
    fi
fi

echo "Configurando arquivos de contrato..."
cd $HOME/domains/chapaamigo.com.br/backend
bash ./setup_contract.sh

echo "Starting backend..."
cd $HOME/domains/chapaamigo.com.br/backend
bash ./start_backend.sh

echo "Verifying backend started..."
sleep 5
if pgrep -f "python3 -m app.api" > /dev/null; then
    echo "Backend successfully started!"
    ps aux | grep "python3 -m app.api" | grep -v grep
else
    echo "Failed to start backend. Check logs for details."
    tail -n 20 $HOME/logs/backend.log
fi

echo "Setting up cron job to ensure backend stays running..."
if command -v crontab >/dev/null 2>&1; then
    (crontab -l 2>/dev/null || echo "") | grep -v "monitor_backend.sh" | cat - $HOME/domains/chapaamigo.com.br/backend/crontab.txt | crontab -
    echo "Cron job set up successfully."
else
    echo "Warning: crontab command not found. Unable to set up automatic monitoring."
    echo "You can manually run the monitor script with: bash $HOME/domains/chapaamigo.com.br/backend/monitor_backend.sh"
fi

echo "Done! Backend should now be running and monitored."

echo ""
echo "Para verificar o status do backend a qualquer momento, execute:"
echo "  - Para verificar se o processo está rodando: ps aux | grep 'python3 -m app.api' | grep -v grep"
echo "  - Para ver os logs em tempo real: tail -f \$HOME/logs/backend.log"
echo "  - Para reiniciar o backend: \$HOME/domains/chapaamigo.com.br/backend/restart_backend.sh"
