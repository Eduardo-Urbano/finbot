from fastapi import APIRouter

from app.api.schemas import Mensagem, Pergunta, Resposta
from app.config.settings import settings
from app.servicos import chat


router = APIRouter()


@router.get("/saude")
def saude():
    return {
        "status": "ok",
        "provedor": settings.llm_provedor,
        "modelo": settings.modelo,
    }


@router.post("/chat", response_model=Resposta)
def perguntar(p: Pergunta):
    return chat.perguntar(p.mensagem, p.sessao, p.usuario)


@router.get(
    "/sessoes/{sessao}/mensagens",
    response_model=list[Mensagem],
)
def mensagens(sessao: str):
    return chat.historico(sessao)