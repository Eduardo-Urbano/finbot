from langchain_core.messages import AIMessage, HumanMessage

from app.agents.chatbot import responder
from app.llm.observabilidade import callbacks, rastrear


_memoria: dict[str, list] = {}


def perguntar(
    pergunta: str,
    sessao: str,
    usuario: str = "anonimo",
) -> dict:
    historico = _memoria.setdefault(sessao, [])

    with rastrear(sessao, usuario):
        resposta = responder(
            historico,
            pergunta,
            callbacks=callbacks(),
        )

    historico += [
        HumanMessage(pergunta),
        AIMessage(resposta.content),
    ]

    return {"resposta": resposta.content}


def historico(sessao: str) -> list[dict]:
    return [
        {
            "papel": "user" if mensagem.type == "human" else "assistant",
            "conteudo": mensagem.content,
        }
        for mensagem in _memoria.get(sessao, [])
    ]
