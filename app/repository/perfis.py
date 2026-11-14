"""Memória de LONGO prazo: o perfil do usuário."""
from app.repository import mongo


def _colecao():
    return mongo.banco()["perfis"]


def salvar_perfil(usuario: str, dados: dict) -> None:
    _colecao().update_one(
        {"usuario": usuario},
        {"$set": {"usuario": usuario, **dados}},
        upsert=True,
    )


def obter_perfil(usuario: str) -> dict:
    return _colecao().find_one(
        {"usuario": usuario},
        {"_id": 0},
    ) or {"usuario": usuario}


def texto_perfil(usuario: str) -> str:
    """Perfil em texto, pronto para entrar no prompt de sistema."""
    p = obter_perfil(usuario)
    partes = [
        f"{campo}: {p[campo]}"
        for campo in ("nome", "objetivo", "experiencia")
        if p.get(campo)
    ]
    return "; ".join(partes) or "não informado"