# ChapaAmigo Backend - Arquitetura MVC

Este documento descreve a nova organização do backend seguindo o padrão MVC (Model-View-Controller).

## Estrutura de Diretórios

```
backend/app/
├── __init__.py              # Inicialização do módulo
├── app.py                   # Aplicação Flask principal (Factory Pattern)
├── api.py                   # Compatibilidade com versão anterior
├── config.py                # Configurações da aplicação
├── controllers/             # Controllers (Lógica de negócio)
│   ├── __init__.py
│   ├── pdf_controller.py    # Controller para operações PDF
│   ├── image_controller.py  # Controller para operações de imagem
│   └── carousel_controller.py # Controller para carousel
├── models/                  # Models (Estruturas de dados)
│   └── __init__.py          # Modelos de dados (FileUpload, PdfProcessingRequest, etc.)
├── services/                # Services (Lógica de negócio core)
│   ├── __init__.py
│   ├── pdf_service.py       # Processamento de PDF (ex-processPdf.py)
│   ├── extract_service.py   # Extração de dados (ex-extractPdfData.py)
│   ├── unlock_service.py    # Desbloqueio de PDF (ex-unlockPdf.py)
│   └── carousel_service.py  # Gerenciamento de carousel
├── utils/                   # Utilities (Funções auxiliares)
│   ├── __init__.py
│   ├── imageUtils.py        # Utilitários de imagem
│   ├── pdfUtils.py          # Utilitários de PDF
│   ├── logging_config.py    # Configuração de logging
│   └── path_config.py       # Configuração de caminhos
└── views/                   # Views (Rotas/Endpoints)
    ├── __init__.py
    ├── pdf_routes.py         # Rotas para PDF
    ├── image_routes.py       # Rotas para imagens
    └── carousel_routes.py    # Rotas para carousel
```

## Padrão MVC Implementado

### Models (`models/`)

- **Responsabilidade**: Definir estruturas de dados e modelos de domínio
- **Arquivos**:
  - `FileUpload`: Modelo para arquivos carregados
  - `PdfProcessingRequest`: Modelo para solicitações de processamento PDF
  - `ExtractedData`: Modelo para dados extraídos
  - `CarouselImage`: Modelo para imagens do carousel

### Views (`views/`)

- **Responsabilidade**: Definir rotas HTTP e gerenciar requisições/respostas
- **Arquivos**:
  - `pdf_routes.py`: Endpoints relacionados a PDF
  - `image_routes.py`: Endpoints relacionados a imagens
  - `carousel_routes.py`: Endpoints relacionados ao carousel

### Controllers (`controllers/`)

- **Responsabilidade**: Processar requisições, validar dados e orquestrar services
- **Arquivos**:
  - `pdf_controller.py`: Lógica de controle para PDF
  - `image_controller.py`: Lógica de controle para imagens
  - `carousel_controller.py`: Lógica de controle para carousel

### Services (`services/`)

- **Responsabilidade**: Lógica de negócio core e integração com sistemas externos
- **Arquivos**:
  - `pdf_service.py`: Processamento e manipulação de PDF
  - `extract_service.py`: Extração de dados de documentos
  - `unlock_service.py`: Desbloqueio de PDFs protegidos
  - `carousel_service.py`: Gerenciamento de imagens do carousel

### Utils (`utils/`)

- **Responsabilidade**: Funções auxiliares e utilitários compartilhados
- **Arquivos**:
  - `imageUtils.py`: Funções para manipulação de imagens
  - `pdfUtils.py`: Funções utilitárias para PDF
  - `logging_config.py`: Configuração de logs
  - `path_config.py`: Configuração de caminhos

## Principais Endpoints

### PDF Operations

- `POST /upload-pdf` - Upload de arquivo PDF
- `POST /process-pdf` - Processamento de PDF
- `POST /crop-pdf` - Recorte de PDF

### Image Operations

- `POST /upload-image` - Upload de imagem

### Carousel Operations

- `GET /carousel-config` - Obter configuração do carousel
- `GET /carousel-images` - Listar imagens do carousel
- `POST /upload-carousel-image` - Upload de imagem para carousel
- `POST /delete-carousel-image` - Excluir imagem do carousel
- `POST /toggle-carousel-image` - Alternar status de imagem
- `POST /reorder-carousel-images` - Reordenar imagens
- `GET /carousel-image/<filename>` - Servir imagem do carousel

## Compatibilidade

O arquivo `api.py` foi mantido para compatibilidade com versões anteriores, importando a nova estrutura MVC. Isso garante que integrações existentes continuem funcionando sem modificações.

## Como Executar

A aplicação pode ser iniciada das seguintes formas:

1. **Via app.py (recomendado)**:

```python
from app import create_app
app = create_app()
```

2. **Via api.py (compatibilidade)**:

```python
from api import app
```

3. **Diretamente**:

```bash
python -m app.app
```

## Benefícios da Nova Arquitetura

1. **Separação de Responsabilidades**: Cada camada tem uma responsabilidade específica
2. **Manutenibilidade**: Código mais organizado e fácil de manter
3. **Testabilidade**: Componentes isolados facilitam testes unitários
4. **Escalabilidade**: Estrutura permite fácil adição de novas funcionalidades
5. **Reutilização**: Services e Utils podem ser reutilizados entre diferentes controllers
6. **Compatibilidade**: Mantém funcionamento com integrações existentes
