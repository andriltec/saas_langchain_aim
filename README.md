# SaaS com LangChain e React

Este projeto é uma aplicação SaaS que utiliza LangChain no backend com FastAPI e React no frontend, com funcionalidades especiais para processamento de transcrições do YouTube.

## Estrutura do Projeto

```
saas_langchain_front/
├── backend/
│   ├── main.py              # API FastAPI
│   ├── requirements.txt     # Dependências Python
│   ├── loaders/            
│   │   └── youtube_loader.py # Loader para transcrições do YouTube
│   ├── tests/              
│   │   └── test_youtube_loader.py # Testes do YouTube Loader
│   └── instructions/        
│       └── LoaderYoutube.md  # Documentação detalhada do YouTube Loader
└── frontend/                # Aplicação React
```

## Requisitos

### Backend
- Python 3.9 ou superior
- FastAPI e Uvicorn para a API
- LangChain e LangChain Community
- youtube-transcript-api e pytube para processamento de vídeos do YouTube
- Outras dependências listadas em `requirements.txt`

### Frontend
- Node.js
- npm ou yarn
- React

## Configuração do Ambiente

1. **Backend**

```bash
# Criar e ativar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Instalar dependências Python
pip install -r requirements.txt

# Iniciar servidor backend
cd backend
uvicorn main:app --reload
```

O backend estará disponível em `http://localhost:8000`

2. **Frontend**

```bash
# Instalar dependências do React
cd frontend
npm install

# Iniciar servidor de desenvolvimento
npm start
```

O frontend estará disponível em `http://localhost:3000`

## Endpoints da API

### GET /
- Retorna uma mensagem de status da API

### POST /process
- Processa texto usando LangChain
- Corpo da requisição:
  ```json
  {
    "text": "Seu texto aqui"
  }
  ```

### POST /youtube/transcript
- Extrai e processa transcrições de vídeos do YouTube
- Corpo da requisição:
  ```json
  {
    "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "add_video_info": false,
    "language": ["en"],
    "translation": null,
    "transcript_format": null,
    "chunk_size_seconds": null
  }
  ```
- Para mais detalhes, consulte a [documentação completa do YouTube Loader](backend/instructions/LoaderYoutube.md)

## Documentação

### API
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Loaders
- [Documentação do YouTube Loader](backend/instructions/LoaderYoutube.md)

## Desenvolvimento

1. O backend está configurado com CORS para aceitar requisições do frontend (`http://localhost:3000`)
2. O frontend está configurado para desenvolvimento com hot-reload
3. Modificações no código do backend com `--reload` ativado serão automaticamente recarregadas
4. Testes unitários disponíveis para os loaders

## Testes

```bash
# Executar testes do YouTube Loader
cd backend
python -m pytest tests/test_youtube_loader.py
```

## Funcionalidades

### YouTube Loader
- Extração de transcrições de vídeos do YouTube
- Suporte a múltiplos idiomas e traduções
- Formatação flexível (texto completo ou chunks)
- Extração de metadados do vídeo
- Tratamento robusto de erros

## Próximos Passos

- [x] Implementar YouTube Loader
- [x] Adicionar testes para o YouTube Loader
- [x] Documentar funcionalidades
- [ ] Implementar processamento adicional com LangChain
- [ ] Adicionar autenticação
- [ ] Melhorar interface do usuário
- [ ] Configurar Docker
- [ ] Preparar para deploy
- [ ] Implementar sistema de cache para o YouTube Loader
- [ ] Adicionar suporte a mais serviços de vídeo