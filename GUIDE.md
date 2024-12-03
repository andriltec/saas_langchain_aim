# Guia de Desenvolvimento e Padrões do Projeto

Este guia fornece uma explicação detalhada sobre a estrutura do projeto, padrões utilizados e funcionalidades de cada componente.

## Estrutura de Diretórios

```
saas_langchain_front/
├── backend/                # Servidor FastAPI + LangChain
│   ├── main.py            # Arquivo principal da API
│   └── requirements.txt   # Dependências Python
└── frontend/              # Aplicação React
    ├── public/            # Arquivos públicos estáticos
    └── src/               # Código fonte React
        ├── components/    # Componentes React reutilizáveis
        ├── pages/         # Páginas da aplicação
        ├── services/      # Serviços de API
        └── utils/         # Funções utilitárias
```

## Backend (FastAPI + LangChain)

### main.py
Este é o arquivo principal do backend que configura o servidor FastAPI e define os endpoints da API.

#### Estrutura Básica
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
```
- `FastAPI()`: Cria uma instância do aplicativo FastAPI
- `CORSMiddleware`: Configura o CORS para permitir requisições do frontend

#### Modelos de Dados (Pydantic)
```python
class InputData(BaseModel):
    text: str
```
- `BaseModel`: Classe base do Pydantic para validação de dados
- Define a estrutura dos dados que a API aceita/retorna

#### Endpoints
```python
@app.get("/")
async def root():
    return {"message": "LangChain API is running"}

@app.post("/process")
async def process_data(data: InputData):
    return {"result": f"Processed: {data.text}"}
```
- Decoradores `@app.get()` e `@app.post()`: Definem rotas HTTP
- Funções assíncronas: Permitem processamento assíncrono eficiente
- Tipagem de parâmetros: Garante validação automática dos dados

## Frontend (React)

### Componentes React

#### Estrutura Básica de um Componente
```javascript
import React, { useState, useEffect } from 'react';

const MyComponent = ({ prop1, prop2 }) => {
  // Estados locais
  const [data, setData] = useState(null);

  // Efeitos colaterais
  useEffect(() => {
    // Código executado na montagem do componente
  }, []);

  return (
    <div>
      {/* JSX do componente */}
    </div>
  );
};
```

#### Hooks Comuns
- `useState`: Gerencia estado local do componente
- `useEffect`: Lida com efeitos colaterais (ex: chamadas API)
- `useCallback`: Memoriza funções
- `useMemo`: Memoriza valores calculados

### Serviços de API

#### Estrutura de um Serviço
```javascript
// src/services/api.js
const API_URL = 'http://localhost:8000';

export const processText = async (text) => {
  try {
    const response = await fetch(`${API_URL}/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};
```

### Padrões de Código

#### Backend
1. **Validação de Dados**
   - Use modelos Pydantic para validação
   - Defina tipos explícitos para parâmetros de função

2. **Tratamento de Erros**
   - Use try/except para capturar exceções
   - Retorne respostas HTTP apropriadas

3. **Documentação**
   - Documente funções com docstrings
   - Use tipos para melhor autocompletar

#### Frontend
1. **Componentes**
   - Um componente por arquivo
   - Nomes em PascalCase
   - Props tipadas com PropTypes ou TypeScript

2. **Estado**
   - Use hooks para gerenciar estado
   - Evite estado global desnecessário
   - Mantenha estado o mais local possível

3. **Estilização**
   - Use CSS Modules ou styled-components
   - Mantenha estilos próximos aos componentes

## Padrões de Nomenclatura

### Backend
- **Arquivos**: snake_case (ex: `main.py`, `database_utils.py`)
- **Classes**: PascalCase (ex: `InputData`, `UserModel`)
- **Funções**: snake_case (ex: `process_data`, `get_user`)
- **Variáveis**: snake_case (ex: `user_input`, `api_key`)

### Frontend
- **Arquivos de Componente**: PascalCase (ex: `Button.jsx`, `UserCard.jsx`)
- **Arquivos de Utilidade**: camelCase (ex: `apiService.js`, `formatUtils.js`)
- **Funções**: camelCase (ex: `handleSubmit`, `fetchData`)
- **Variáveis**: camelCase (ex: `userData`, `isLoading`)

## Boas Práticas

1. **Código Limpo**
   - Funções pequenas e focadas
   - Nomes descritivos
   - Comentários apenas quando necessário

2. **Performance**
   - Use lazy loading para componentes grandes
   - Memorize cálculos pesados
   - Otimize renderizações React

3. **Segurança**
   - Sanitize inputs
   - Use HTTPS em produção
   - Implemente rate limiting

4. **Manutenibilidade**
   - Mantenha dependências atualizadas
   - Escreva testes
   - Documente mudanças significativas

## Fluxo de Desenvolvimento

1. **Iniciando uma Nova Feature**
   - Crie um branch específico
   - Planeje a implementação
   - Documente requisitos

2. **Desenvolvimento**
   - Siga os padrões de código
   - Escreva testes
   - Mantenha commits organizados

3. **Code Review**
   - Revise seu próprio código
   - Peça feedback
   - Corrija issues encontrados

4. **Deploy**
   - Teste em ambiente de staging
   - Verifique logs
   - Monitore métricas

## Recursos Úteis

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Documentação React](https://reactjs.org/docs/getting-started.html)
- [Documentação LangChain](https://python.langchain.com/docs/get_started/introduction)
- [Melhores Práticas React](https://reactjs.org/docs/thinking-in-react.html)
