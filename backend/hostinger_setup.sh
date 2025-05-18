#!/bin/bash
# Script para configurar o backend para execução persistente na Hostinger

echo "================================================"
echo "   CONFIGURAÇÃO DO SERVIDOR BACKEND CHAPAAMIGO  "
echo "================================================"
echo ""

# Defina o diretório do backend
BACKEND_DIR=$HOME/domains/chapaamigo.com.br/backend
LOG_DIR=$HOME/logs
PID_FILE=$HOME/backend.pid

echo "📁 Diretório do backend: $BACKEND_DIR"
echo "📁 Diretório de logs: $LOG_DIR"
echo "📄 Arquivo PID: $PID_FILE"
echo ""

# Crie o diretório de logs se não existir
mkdir -p $LOG_DIR
echo "✅ Diretório de logs criado em $LOG_DIR"

# Dê permissão de execução aos scripts
chmod +x $BACKEND_DIR/*.sh
echo "✅ Permissões de execução concedidas aos scripts"

# Encerre qualquer instância em execução
echo ""
echo "🔄 Verificando instâncias em execução..."
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat $PID_FILE)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "   Encerrando processo anterior (PID: $OLD_PID)..."
        kill -9 $OLD_PID
    fi
    rm -f $PID_FILE
fi

# Matar qualquer processo Python relacionado à API que possa estar rodando
pkill -f "python.*app.api" 2>/dev/null
echo "✅ Processos antigos encerrados"

# Configure o crontab para monitorar e manter o servidor rodando
echo ""
echo "🔄 Configurando crontab para monitorar o backend..."
echo ""
echo "🔄 Configurando tarefas agendadas para monitoramento..."

# Verificar se o comando crontab está disponível
if command -v crontab >/dev/null 2>&1; then
    echo "   Configurando via crontab..."
    (crontab -l 2>/dev/null || echo "") | grep -v "monitor_backend.sh" | grep -v "restart_backend.sh" > /tmp/crontmp
    echo "# Monitorar backend a cada 5 minutos" >> /tmp/crontmp
    echo "*/5 * * * * /bin/bash $BACKEND_DIR/monitor_backend.sh >> $LOG_DIR/cron.log 2>&1" >> /tmp/crontmp
    echo "# Reiniciar o backend diariamente às 4h da manhã para manutenção" >> /tmp/crontmp
    echo "0 4 * * * /bin/bash $BACKEND_DIR/restart_backend.sh >> $LOG_DIR/cron.log 2>&1" >> /tmp/crontmp
    crontab /tmp/crontmp
    rm -f /tmp/crontmp
    echo "✅ Crontab configurado com sucesso"
else
    echo "⚠️ O comando crontab não está disponível neste sistema"
    echo "   Você precisa configurar as tarefas agendadas via painel da Hostinger:"
    echo ""
    echo "   1. Acesse o hPanel da Hostinger: https://hpanel.hostinger.com/"
    echo "   2. Vá para 'Avançado' > 'Cron Jobs'"
    echo "   3. Adicione as seguintes tarefas:"
    echo ""
    echo "      • Executar a cada 5 minutos:"
    echo "        /bin/bash $BACKEND_DIR/monitor_backend.sh >> $LOG_DIR/cron.log 2>&1"
    echo ""
    echo "      • Executar diariamente às 4h da manhã:"
    echo "        /bin/bash $BACKEND_DIR/restart_backend.sh >> $LOG_DIR/cron.log 2>&1"
    echo ""
    echo "✅ Instruções para configuração manual de tarefas agendadas exibidas"
fi

# Inicie o backend
echo ""
echo "🚀 Iniciando o backend..."
cd $BACKEND_DIR
bash ./start_backend.sh

# Verifique se o backend foi iniciado com sucesso
sleep 3
if pgrep -f "python.*app.api" > /dev/null; then
    echo "✅ Backend iniciado com sucesso!"
    echo "   PID: $(cat $PID_FILE)"
    echo ""
    echo "   Verifique os logs em: $LOG_DIR/backend.log"
    echo "   Para monitorar em tempo real: tail -f $LOG_DIR/backend.log"
else
    echo "❌ Falha ao iniciar o backend. Verifique os logs para mais detalhes."
fi

echo ""
echo "================================================"
echo "       CONFIGURAÇÃO CONCLUÍDA COM SUCESSO       "
echo "================================================"
echo ""
echo "📋 Comandos úteis:"
echo "   • Verificar status: bash $BACKEND_DIR/check_status.sh"
echo "   • Reiniciar servidor: bash $BACKEND_DIR/restart_backend.sh"
echo "   • Ver logs: tail -f $LOG_DIR/backend.log"
echo ""
echo "💡 O servidor continuará rodando mesmo após fechar o terminal SSH"
echo "   Isso é possível graças à combinação de nohup, disown e monitoramento via cron"
echo "================================================"
