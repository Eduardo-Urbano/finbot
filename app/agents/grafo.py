
"""O grafo principal do FinBot.

Grafo = NÓS (funções) + ARESTAS (quem vem depois) + ESTADO (o que passa de nó em nó).

Aula 3: START -> chatbot -> END
(+ checkpointer = memória de curto prazo)
"""

from functools import lru_cache
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from app.agents.chatbot import no_chatbot
from app.llm.observabilidade import callbacks, rastrear
from app.repository import checkpointer, conversas, perfis
from app.utils.mensagens import conversa_limpa


# Estado do grafo: mensagens e perfil do usuário.
class EstadoChat(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    perfil: str


# ---------- Montagem ----------
def montar_grafo(memoria=None):
    g = StateGraph(EstadoChat)
    g.add_node("chatbot", no_chatbot)
    g.add_edge(START, "chatbot")
    g.add_edge("chatbot", END)

    return g.compile(checkpointer=memoria)


@lru_cache
def grafo():
    """Compila uma única vez, com a memória no MongoDB."""
    return montar_grafo(checkpointer.criar_checkpointer())


def executar(pergunta: str, sessao: str, usuario: str = "anonimo") -> dict:
    # thread_id identifica a conversa.
    config = {
        "configurable": {"thread_id": sessao},
        "callbacks": callbacks(),
    }

    # Só a pergunta nova entra; o histórico anterior vem do checkpointer.
    entrada = {
        "messages": [HumanMessage(pergunta)],
        "perfil": perfis.texto_perfil(usuario),
    }

    with rastrear(sessao, usuario):
        estado = grafo().invoke(entrada, config)

    # Registra ou atualiza a conversa na lista do usuário.
    conversas.registrar(sessao, usuario, pergunta)

    final = estado["messages"][-1]

    return {
        "resposta": final.content,
        "agente": "conversa",
        "fontes": [],
    }


def historico(sessao: str) -> list[dict]:
    """Mensagens da sessão lidas do checkpointer."""
    estado = grafo().get_state(
        {"configurable": {"thread_id": sessao}}
    )

    mensagens = estado.values.get("messages", []) if estado else []

    return [
        {
            "papel": "user" if m.type == "human" else "assistant",
            "conteudo": m.content,
            "agente": m.name,
        }
        for m in conversa_limpa(mensagens, limite=1000)
    ]


if __name__ == "__main__":
    # python -m app.agents.grafo imprime o desenho do grafo em Mermaid.
    print(montar_grafo().get_graph(xray=True).draw_mermaid())
