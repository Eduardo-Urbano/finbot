"""Observabilidade com Langfuse.

Cada pergunta pode gerar um trace com chamadas ao LLM,
entrada, saída, tokens e tempo de execução.

Sem as chaves no .env, o FinBot continua funcionando
normalmente, apenas sem registrar traces.
"""

import os
from contextlib import contextmanager

from app.config.settings import settings


if settings.langfuse_ativo:
    os.environ.setdefault(
        "LANGFUSE_PUBLIC_KEY",
        settings.langfuse_public_key,
    )
    os.environ.setdefault(
        "LANGFUSE_SECRET_KEY",
        settings.langfuse_secret_key.get_secret_value(),
    )
    os.environ.setdefault("LANGFUSE_HOST", settings.langfuse_host)
    os.environ.setdefault("LANGFUSE_TRACING_ENVIRONMENT", "local")


def cliente_langfuse():
    from langfuse import get_client

    return get_client()


def callbacks() -> list:
    if not settings.langfuse_ativo:
        return []

    from langfuse.langchain import CallbackHandler

    return [CallbackHandler()]


@contextmanager
def rastrear(sessao: str, usuario: str, nome: str = "chat"):
    if not settings.langfuse_ativo:
        yield
        return

    from langfuse import propagate_attributes

    with propagate_attributes(
        session_id=sessao,
        user_id=usuario,
        trace_name=nome,
    ):
        yield

def config_prompt(prompt) -> dict:
    """Liga a chamada do LLM à versão do prompt usada."""

    # Prompt local não possui versão no Langfuse.
    if getattr(prompt, "is_fallback", True):
        return {}

    # Associa a geração à versão do prompt no Langfuse.
    return {"metadata": {"langfuse_prompt": prompt}}