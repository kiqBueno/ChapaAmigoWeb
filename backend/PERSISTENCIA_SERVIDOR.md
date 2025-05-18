# Guia para Servidor Persistente na Hostinger

Este guia explica como manter o servidor backend funcionando continuamente na Hostinger, mesmo depois de fechar o terminal SSH.

## Problema

Em servidores compartilhados como o da Hostinger, quando você executa um script pelo terminal SSH e fecha a conexão, os processos iniciados são automaticamente terminados. Isso ocorre porque o sistema operacional envia um sinal SIGHUP (hangup) para todos os processos filhos daquela sessão.

## Solução

Foram implementados vários mecanismos para garantir que o servidor continue rodando:

1. **nohup + disown**: O script `start_backend.sh` usa `nohup` e `disown` para desvincular o processo do terminal
2. **Monitoramento via cron**: Um script de monitoramento é executado a cada 5 minutos para verificar e reiniciar o servidor se necessário
3. **Reinício automático**: O servidor é reiniciado diariamente às 4h da manhã para evitar problemas

## Instruções de Uso

### Configuração Inicial

Ao implantar no servidor Hostinger pela primeira vez, execute:

```bash
cd ~/domains/chapaamigo.com.br/backend
bash hostinger_setup.sh
```

Isso vai:

- Iniciar o servidor em modo persistente
- Verificar se crontab está disponível para configuração automática
- Exibir instruções para configuração manual se necessário

#### Configuração de Tarefas Agendadas (Cron Jobs) no Painel da Hostinger

Como o comando `crontab` não está disponível diretamente no shell da Hostinger, você precisa configurar as tarefas agendadas manualmente através do painel de controle:

1. Acesse o hPanel da Hostinger: https://hpanel.hostinger.com/
2. Navegue até "Avançado" > "Cron Jobs"
3. Adicione as seguintes tarefas:

   **Para monitoramento a cada 5 minutos:**

   - Período: A cada 5 minutos
   - Comando: `/bin/bash /u279915365/domains/chapaamigo.com.br/backend/monitor_backend.sh >> /u279915365/logs/cron.log 2>&1`

   **Para reinicialização diária:**

   - Período: Uma vez ao dia
   - Hora: 4:00
   - Comando: `/bin/bash /u279915365/domains/chapaamigo.com.br/backend/restart_backend.sh >> /u279915365/logs/cron.log 2>&1`

### Comandos Úteis

1. **Verificar status do servidor**:

   ```bash
   bash ~/domains/chapaamigo.com.br/backend/check_status.sh
   ```

2. **Reiniciar manualmente o servidor**:

   ```bash
   bash ~/domains/chapaamigo.com.br/backend/restart_backend.sh
   ```

3. **Monitorar logs em tempo real**:
   ```bash
   tail -f ~/logs/backend.log
   ```

### Arquivos Importantes

- **start_backend.sh**: Inicia o servidor em modo persistente
- **monitor_backend.sh**: Verifica e reinicia o servidor se ele cair
- **restart_backend.sh**: Força a reinicialização do servidor
- **check_status.sh**: Mostra o status detalhado do servidor
- **hostinger_setup.sh**: Configura todo o ambiente

## Métodos Alternativos para Persistência

### Usar o Painel da Hostinger para Iniciar o Servidor

Se o método de `nohup` + `disown` + monitoramento não for suficiente, você pode usar o painel da Hostinger para garantir que o servidor seja executado:

1. Crie um arquivo `start_production.sh`:

   ```bash
   #!/bin/bash
   cd /u279915365/domains/chapaamigo.com.br/backend
   bash start_backend.sh
   ```

2. Configure um Cron Job no painel da Hostinger para executar esse script:
   - A cada reinicialização (se disponível)
   - Ou a cada hora para garantir que o servidor esteja sempre rodando

### Usar .htaccess para Processos em Background

Em alguns planos da Hostinger, você pode configurar um arquivo `.htaccess` para iniciar processos em background. Consulte a documentação da Hostinger para saber se isso é suportado no seu plano.

## Solução de Problemas

Se o servidor continuar parando:

1. Verifique se as tarefas agendadas estão configuradas corretamente no painel da Hostinger:

   - Acesse hPanel > Avançado > Cron Jobs
   - Verifique se as tarefas estão ativas e com os comandos corretos

2. Verifique os logs:

   ```bash
   tail -f ~/logs/backend.log
   tail -f ~/logs/cron.log
   ```

3. Verifique o status do servidor:

   ```bash
   bash ~/domains/chapaamigo.com.br/backend/check_status.sh
   ```

4. Verifique se existem restrições de recursos na sua conta Hostinger:

   - Limites de CPU
   - Limites de memória
   - Políticas de processos em segundo plano

5. Se necessário, entre em contato com o suporte da Hostinger e explique que você precisa manter um processo Python rodando em segundo plano para seu aplicativo web.
