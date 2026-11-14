from app.config.settings import settings
from app.prompts import catalogo


def test_memoria_curta_recupera_historico(api, falso):
    api.post(
        "/chat",
        json={
            "mensagem": "Meu nome é Ana",
            "sessao": "memoria-1",
            "usuario": "ana",
        },
    )

    api.post(
        "/chat",
        json={
            "mensagem": "Qual é meu nome?",
            "sessao": "memoria-1",
            "usuario": "ana",
        },
    )

    textos = [m.content for m in falso.vistas]

    assert "Meu nome é Ana" in textos
    assert "Qual é meu nome?" in textos


def test_perfil_pode_ser_salvo_e_recuperado(api):
    resposta = api.put(
        "/usuarios/ana/perfil",
        json={
            "nome": "Ana",
            "objetivo": "Reserva de emergência",
            "experiencia": "Iniciante",
        },
    )

    assert resposta.status_code == 200

    perfil = api.get("/usuarios/ana/perfil")

    assert perfil.status_code == 200
    assert perfil.json()["nome"] == "Ana"
    assert perfil.json()["objetivo"] == "Reserva de emergência"
    assert perfil.json()["experiencia"] == "Iniciante"


def test_conversas_sao_separadas_por_usuario(api):
    api.post(
        "/chat",
        json={
            "mensagem": "Pergunta da Ana",
            "sessao": "sessao-ana",
            "usuario": "ana",
        },
    )

    api.post(
        "/chat",
        json={
            "mensagem": "Pergunta do João",
            "sessao": "sessao-joao",
            "usuario": "joao",
        },
    )

    conversas_ana = api.get("/usuarios/ana/conversas").json()
    conversas_joao = api.get("/usuarios/joao/conversas").json()

    sessoes_ana = [c["sessao"] for c in conversas_ana]
    sessoes_joao = [c["sessao"] for c in conversas_joao]

    assert "sessao-ana" in sessoes_ana
    assert "sessao-joao" not in sessoes_ana
    assert "sessao-joao" in sessoes_joao
    assert "sessao-ana" not in sessoes_joao


def test_prompt_usa_fallback_local_sem_langfuse(monkeypatch):
    monkeypatch.setattr(settings, "langfuse_public_key", None)
    monkeypatch.setattr(settings, "langfuse_secret_key", None)

    prompt = catalogo.obter("sistema")

    assert prompt.is_fallback is True
    assert prompt.version == "local"
    assert prompt.compile(perfil="Ana") != ""
