"""Lista de conversas de cada usuário."""
from datetime import datetime, timezone

from app.repository import mongo


def _colecao():
    return mongo.banco()["conversas"]


def registrar(sessao: str, usuario: str, primeira_pergunta: str) -> None:
    agora = datetime.now(timezone.utc)

    _colecao().update_one(
        {"sessao": sessao},
        {
            "$set": {"atualizada_em": agora},
            "$setOnInsert": {
                "sessao": sessao,
                "usuario": usuario,
                "titulo": primeira_pergunta[:60],
                "criada_em": agora,
            },
        },
        upsert=True,
    )


def listar(usuario: str) -> list[dict]:
    return list(
        _colecao()
        .find({"usuario": usuario}, {"_id": 0})
        .sort("atualizada_em", -1)
        .limit(20)
    )