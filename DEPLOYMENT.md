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

## Segurança

- Considere adicionar HTTPS para mais segurança.
- Os scripts de backend estão configurados para execução contínua e monitoramento automático.
