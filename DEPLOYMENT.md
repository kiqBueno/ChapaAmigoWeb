# ChapaAmigo Web - Guia de Implantação

## Estrutura do Projeto

- **frontend**: Aplicação React/TypeScript
- **backend**: API Flask/Python para processamento de PDF

## Requisitos do Servidor

- Python 3.8+
- Node.js 16+ (apenas para build do frontend)
- Servidor web (Apache ou Nginx)

## Preparação para Implantação

### Frontend

1. Build da aplicação React:

```bash
cd frontend
npm install
npm run build
```

2. Copie os arquivos da pasta `dist` para o diretório raiz do seu domínio no servidor.
3. Certifique-se de que o arquivo `.htaccess` está na raiz para lidar com rotas do SPA.

### Backend

1. Copie a pasta `backend` para o servidor.
2. No servidor, execute o script de configuração:

```bash
cd backend
chmod +x setup_server.sh
./setup_server.sh
```

## Estrutura de Arquivos no Servidor

```
/u279915365/domains/chapaamigo.com.br/
├── public_html/           # Arquivos do frontend (conteúdo da pasta dist)
│   ├── index.html
│   ├── .htaccess          # Arquivo para roteamento
│   └── [outros arquivos de build]
├── backend/               # Código do backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   └── [outros arquivos]
│   ├── setup_server.sh
│   ├── start_backend.sh   # Script para iniciar o servidor
│   └── monitor_backend.sh # Script para monitoramento
└── logs/                  # Logs da aplicação
    ├── backend.log
    └── monitor.log
```

## Manutenção

- Para verificar o status do backend: `ps aux | grep app.api`
- Para reiniciar manualmente: `bash /u279915365/domains/chapaamigo.com.br/backend/monitor_backend.sh`
- Logs:
  - Backend: `/u279915365/domains/chapaamigo.com.br/logs/backend.log`
  - Monitoramento: `/u279915365/domains/chapaamigo.com.br/logs/monitor.log`

## Troubleshooting

1. Problema com CORS: Verifique a configuração CORS no arquivo `api.py`.
2. Problema com PDF: Certifique-se de que as bibliotecas ReportLab e PyMuPDF estão instaladas.
3. Backend não inicia: Verifique os logs para detalhes do erro.
4. Erro 'calibri.ttf': Substituído pela fonte Helvetica disponível em todos os sistemas.
5. Erro com `setup_contract.sh`: Se o script estiver faltando, crie-o com o conteúdo abaixo:

   ```bash
   #!/bin/bash
   # Script para configurar os arquivos de contrato

   # Diretórios
   BASE_DIR=$HOME/domains/chapaamigo.com.br
   BACKEND_DIR=$BASE_DIR/backend
   STATIC_DIR=$BACKEND_DIR/static
   PUBLIC_DIR=$BASE_DIR/public

   # Verificar se os diretórios existem
   mkdir -p $STATIC_DIR

   # Copiar arquivos de contrato para diretórios apropriados se existirem
   echo "Copiando arquivos de contrato..."

   # Copiar de public para static se existir
   if [ -f "$PUBLIC_DIR/TERMO_FICHA_CADASTRO_PDF.pdf" ]; then
       cp "$PUBLIC_DIR/TERMO_FICHA_CADASTRO_PDF.pdf" "$STATIC_DIR/"
       echo "Arquivo TERMO_FICHA_CADASTRO_PDF.pdf copiado para $STATIC_DIR/"
   fi

   # Copiar de public para static se existir
   if [ -f "$PUBLIC_DIR/Contrato-de-Adesao-aos-Termos-de-Uso-da-Plataforma-CHAPAAMIGO®.pdf" ]; then
       cp "$PUBLIC_DIR/Contrato-de-Adesao-aos-Termos-de-Uso-da-Plataforma-CHAPAAMIGO®.pdf" "$STATIC_DIR/"
       echo "Arquivo Contrato-de-Adesao-aos-Termos-de-Uso-da-Plataforma-CHAPAAMIGO®.pdf copiado para $STATIC_DIR/"
   fi

   echo "Configuração de arquivos de contrato concluída"
   ```

6. Erro com permissões: Assegure-se de que todos os scripts tenham permissões de execução:
   ```bash
   chmod +x *.sh
   ```
7. Erro "crontab: command not found": Se o crontab não estiver disponível no servidor, você pode:
   - Executar o script de monitoramento manualmente: `bash monitor_backend.sh`
   - Solicitar assistência ao suporte da Hostinger para configurar tarefas agendadas

## Segurança

- Considere adicionar HTTPS para mais segurança.
- Os scripts de backend estão configurados para execução contínua e monitoramento automático.
