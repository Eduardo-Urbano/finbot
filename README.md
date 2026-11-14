# FinBot

Assistente educacional sobre investimentos no Brasil, desenvolvido em Python com LangChain, LangGraph e modelos de linguagem.

O projeto permite conversar sobre conceitos financeiros, manter o histórico de conversas e armazenar informações de perfil dos usuários.

## Funcionalidades

- Chat educacional sobre investimentos.
- Integração com Groq, Gemini e Mistral.
- API REST desenvolvida com FastAPI.
- Interface de conversação desenvolvida com Streamlit.
- Memória de curto prazo com LangGraph e MongoDB.
- Persistência de conversas entre reinicializações da API.
- Gerenciamento de perfis por usuário.
- Histórico de conversas separado por usuário.
- Prompts armazenados em arquivos Markdown, com suporte a versionamento pelo Langfuse e fallback local.
- Testes automatizados com Pytest.

## Desenvolvimento por etapas

### Aula 1 — Ambiente e primeiro chat

- Configuração centralizada com Pydantic Settings.
- Integração com os provedores Groq, Gemini e Mistral.
- Fábrica para criação dos modelos de linguagem.
- Prompt de sistema carregado de um arquivo Markdown.
- Chat pelo terminal com histórico de mensagens.
- Testes automatizados com Pytest.

### Aula 2 — API e interface web

- API REST desenvolvida com FastAPI.
- Interface web desenvolvida com Streamlit.
- Comunicação entre frontend e backend.
- Deploy da API no Render.
- Deploy da interface no Streamlit Cloud.

### Aula 3 — Memória e gerenciamento de conversas

- Implementação de grafo de conversação com LangGraph.
- Memória de curto prazo com checkpointer no MongoDB.
- Persistência de perfis e conversas.
- Separação de dados por identificador de usuário.
- Recuperação do histórico de mensagens.
- Catálogo de prompts em arquivos Markdown.
- Integração preparada para gerenciamento de versões de prompts pelo Langfuse.
- Testes automatizados com MongoDB simulado usando mongomock.

## Tecnologias utilizadas

- Python 3.12
- LangChain
- LangGraph
- FastAPI
- Streamlit
- MongoDB / PyMongo
- Pydantic Settings
- Groq, Gemini e Mistral
- Langfuse
- Pytest
- mongomock
- Git e GitHub

## Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/Eduardo-Urbano/finbot.git
cd finbot
```

### 2. Criar e ativar o ambiente virtual

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
python -m pip install -r requirements-dev.txt
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto utilizando o `.env.example` como referência.

Configure:

- O provedor e a respectiva chave de API.
- A conexão com o MongoDB (`MONGO_URL`).
- O nome do banco de dados (`MONGO_BANCO`).
- As credenciais do Langfuse, caso queira utilizar observabilidade e gerenciamento remoto de prompts.

Para desenvolvimento local, o banco utilizado é `finbot_dev`.

As credenciais do Langfuse são opcionais. Sem elas, o projeto utiliza os prompts locais.

### 5. Iniciar a API

```powershell
uvicorn app.main:app --reload
```

A documentação interativa estará disponível em:

`http://127.0.0.1:8000/docs`

### 6. Iniciar a interface web

Em outro terminal, com o ambiente virtual ativado:

```powershell
streamlit run frontend/streamlit_app.py
```

A interface estará disponível no endereço local informado pelo Streamlit.

## Testes

Para executar todos os testes automatizados:

```powershell
python -m pytest -v
```

Os testes utilizam modelos falsos e mongomock para evitar dependência de serviços externos durante sua execução.

## Segurança

- As credenciais ficam armazenadas no arquivo `.env`, que deve permanecer fora do controle de versão.
- O `.env.example` contém apenas as variáveis necessárias para configurar o projeto.
- Não compartilhe chaves de API ou credenciais do MongoDB.
- O identificador de usuário utilizado na interface não representa autenticação. Portanto, não utilize dados pessoais ou informações sensíveis na aplicação pública.

## Links do projeto

| Serviço | Link |
|---|---|
| Chat publicado (Streamlit Cloud) | [FinBot](https://finbot-investimentos.streamlit.app/) |
| API publicada (Render) | [API FinBot](https://finbot-api-yx86.onrender.com) |
| Documentação da API | [Swagger UI](https://finbot-api-yx86.onrender.com/docs) |
| Repositório | [GitHub](https://github.com/Eduardo-Urbano/finbot) |

**Observação:** no plano gratuito do Render, a API pode entrar em suspensão após um período sem utilização. A primeira requisição pode demorar enquanto o serviço é inicializado.

O FinBot é um projeto educacional e não fornece recomendações individuais de investimento.