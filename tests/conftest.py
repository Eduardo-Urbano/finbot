import pytest
from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage

from app.main import app
from app.agents import chatbot
from app.servicos import chat


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
def api(falso):
    chat._memoria.clear()

    with TestClient(app) as cliente:
        yield cliente

    chat._memoria.clear()