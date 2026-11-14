
from app.agents import grafo
from app.repository import conversas, perfis


def perguntar(pergunta: str, sessao: str, usuario: str = "anonimo") -> dict:
    return grafo.executar(pergunta, sessao, usuario)


def historico(sessao: str) -> list[dict]:
    return grafo.historico(sessao)


def listar_conversas(usuario: str) -> list[dict]:
    return conversas.listar(usuario)


def obter_perfil(usuario: str) -> dict:
    return perfis.obter_perfil(usuario)


def salvar_perfil(usuario: str, dados: dict) -> dict:
    perfis.salvar_perfil(usuario, dados)
    return perfis.obter_perfil(usuario)