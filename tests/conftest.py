import mongomock
import pytest
from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver

from app.main import app
from app.agents import chatbot, grafo as grafo_modulo
from app.repository import mongo


class ModeloFalso:
    def __init__(self):
        self.vistas = []

    def invoke(self, mensagens, config=None):
        self.vistas = list(mensagens)
        return AIMessage(content="resposta de teste")


@pytest.fixture
def falso(monkeypatch):
    modelo = ModeloFalso()

    monkeypatch.setattr(
        chatbot.fabrica,
        "criar_modelo",
        lambda: modelo,
    )

    return modelo


@pytest.fixture
def banco_teste(monkeypatch):
    cliente = mongomock.MongoClient()
    banco = cliente["finbot_test"]

    monkeypatch.setattr(
        mongo,
        "banco",
        lambda: banco,
    )

    yield banco

    cliente.close()


@pytest.fixture
def api(falso, banco_teste, monkeypatch):
    memoria = MemorySaver()
    grafo_teste = grafo_modulo.montar_grafo(memoria=memoria)

    monkeypatch.setattr(
        grafo_modulo,
        "grafo",
        lambda: grafo_teste,
    )

    with TestClient(app) as cliente:
        yield cliente
