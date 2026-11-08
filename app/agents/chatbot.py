"""Agente de conversa geral: LLM + prompt de sistema."""

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)

from app.llm import fabrica
from app.prompts import catalogo


def responder(
    historico: list[BaseMessage],
    pergunta: str,
    callbacks: list | None = None,
) -> AIMessage:
    mensagens = (
        [SystemMessage(catalogo.carregar("sistema"))]
        + historico[-10:]
        + [HumanMessage(pergunta)]
    )

    return fabrica.criar_modelo().invoke(
        mensagens,
        config={"callbacks": callbacks or []},
    )