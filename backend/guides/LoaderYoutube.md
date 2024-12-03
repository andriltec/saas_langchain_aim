# YouTube Transcript Loader

## Visão Geral
O YouTube Transcript Loader é um componente especializado para extrair e processar transcrições de vídeos do YouTube. Ele oferece funcionalidades avançadas como suporte a múltiplos idiomas, formatação em chunks de tempo e extração de metadados do vídeo.

## Características Principais
- Extração de transcrições em múltiplos idiomas
- Suporte a tradução de legendas
- Formatação flexível (texto completo ou chunks)
- Extração opcional de metadados do vídeo
- Tratamento robusto de erros

## Requisitos
```bash
pip install youtube-transcript-api pytube langchain-community
```

## Uso Básico

### Endpoint
```
POST /youtube/transcript
```

### Parâmetros da Requisição
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

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| youtube_url | string | Sim | URL do vídeo do YouTube |
| add_video_info | boolean | Não | Se true, inclui metadados do vídeo |
| language | array | Não | Lista de códigos de idioma preferidos |
| translation | string | Não | Código do idioma para tradução |
| transcript_format | string | Não | Formato da transcrição ("CHUNKS" ou null) |
| chunk_size_seconds | integer | Não | Tamanho dos chunks em segundos |

### Exemplos de Uso

#### 1. Obter Transcrição Básica
```python
import requests

response = requests.post("http://localhost:8000/youtube/transcript", json={
    "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "add_video_info": False,
    "language": ["en"]
})

print(response.json())
```

#### 2. Obter Transcrição em Chunks com Informações do Vídeo
```python
import requests

response = requests.post("http://localhost:8000/youtube/transcript", json={
    "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "add_video_info": True,
    "language": ["en", "pt"],
    "transcript_format": "CHUNKS",
    "chunk_size_seconds": 30
})

print(response.json())
```

### Formatos de Resposta

#### Transcrição Básica
```json
{
    "status": "success",
    "data": {
        "text": "Transcrição completa do vídeo...",
        "video_info": {  // Se add_video_info=true
            "title": "Título do Vídeo",
            "description": "Descrição do Vídeo",
            "view_count": 1000,
            "author": "Nome do Autor",
            "length": 300
        }
    }
}
```

#### Transcrição em Chunks
```json
{
    "status": "success",
    "data": [
        {
            "text": "Texto do primeiro chunk...",
            "start": 0,
            "duration": 30,
            "video_info": {  // Se add_video_info=true
                "title": "Título do Vídeo",
                "description": "Descrição do Vídeo",
                "view_count": 1000,
                "author": "Nome do Autor",
                "length": 300
            }
        },
        // ... mais chunks
    ]
}
```

### Tratamento de Erros

O loader inclui tratamento robusto de erros para várias situações comuns:

1. **Legendas Desativadas**
```json
{
    "status": "error",
    "message": "As legendas estão desativadas para este vídeo"
}
```

2. **Legendas Não Encontradas**
```json
{
    "status": "error",
    "message": "Nenhuma legenda encontrada para este vídeo"
}
```

3. **URL Inválida**
```json
{
    "status": "error",
    "message": "URL do YouTube inválida"
}
```

## Estratégia de Implementação

### 1. Extração de ID do Vídeo
- Utiliza expressões regulares para extrair o ID do vídeo da URL
- Suporta múltiplos formatos de URL do YouTube
- Validação robusta para garantir URL válida

### 2. Obtenção de Transcrições
1. Lista todas as transcrições disponíveis para o vídeo
2. Tenta obter a transcrição nos idiomas preferidos
3. Se não encontrar, usa a primeira transcrição disponível
4. Suporta tradução para outro idioma se solicitado

### 3. Processamento de Chunks
- Divide a transcrição em chunks baseados no tempo
- Mantém informações de timestamp para cada chunk
- Garante que o texto seja dividido de forma coerente

### 4. Metadados do Vídeo
- Usa pytube para extrair informações adicionais
- Implementa fallback gracioso quando informações não estão disponíveis
- Cache de informações para evitar requisições repetidas

### 5. Tratamento de Erros
- Tratamento específico para erros comuns
- Mensagens de erro claras e informativas
- Logging para diagnóstico de problemas

## Considerações de Performance

1. **Caching**
- Considere implementar cache de transcrições para vídeos frequentemente acessados
- Cache de metadados do vídeo para reduzir chamadas à API

2. **Otimização de Chunks**
- O tamanho do chunk pode impactar a performance
- Recomendado: 30-60 segundos para melhor balanço

3. **Limites de Taxa**
- Observe os limites de taxa da API do YouTube
- Implemente rate limiting se necessário

## Limitações Conhecidas

1. **Disponibilidade de Legendas**
- Depende da disponibilidade de legendas no vídeo
- Alguns vídeos podem não ter legendas ou ter apenas legendas geradas automaticamente

2. **Qualidade da Tradução**
- A qualidade da tradução depende do serviço do YouTube
- Nem todos os idiomas podem estar disponíveis para tradução

3. **Informações do Vídeo**
- Alguns metadados podem não estar disponíveis para todos os vídeos
- A extração de informações pode falhar em vídeos privados ou restritos

## Próximos Passos

1. **Melhorias Planejadas**
- Implementação de sistema de cache
- Suporte a mais formatos de saída
- Melhor tratamento de legendas geradas automaticamente

2. **Possíveis Extensões**
- Integração com outros serviços de vídeo
- Análise de sentimento do texto
- Extração de palavras-chave
