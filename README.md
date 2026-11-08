# FinBot

Assistente educacional sobre investimentos no Brasil, desenvolvido em Python com LangChain e modelos de linguagem.

## Aula 1 — Ambiente e primeiro chat

Nesta etapa foram implementados:

- Configuração centralizada com Pydantic Settings.
- Integração com os provedores Groq, Gemini e Mistral.
- Fábrica para criação dos modelos de linguagem.
- Prompt de sistema carregado de um arquivo Markdown.
- Chat pelo terminal com histórico de mensagens.
- Testes automatizados com Pytest.

## Tecnologias utilizadas

- Python 3.12
- LangChain
- Groq
- Pydantic Settings
- Pytest

## Como executar

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
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

Crie um arquivo `.env` na raiz do projeto, utilizando o `.env.example` como referência.

Configure seu provedor e informe a respectiva chave de API.

### 5. Iniciar o FinBot

```powershell
python -m scripts.chat_terminal
```

Para encerrar a conversa, digite `sair`.

## Testes

Para executar os testes automatizados:

```powershell
python -m pytest -v
```

## Segurança

As credenciais de API ficam armazenadas no arquivo `.env`, que está listado no `.gitignore` e não deve ser enviado ao GitHub.

O arquivo `.env.example` contém apenas as variáveis necessárias para configurar o projeto, sem credenciais reais.