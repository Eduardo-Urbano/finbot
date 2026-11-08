def test_saude(api):
    assert api.get("/saude").json()["status"] == "ok"


def test_chat_responde(api):
    r = api.post("/chat", json={"mensagem": "Oi!", "sessao": "s1"})
    assert r.status_code == 200
    assert "resposta de teste" in r.json()["resposta"]


def test_chat_envia_o_historico_ao_modelo(api, falso):
    api.post("/chat", json={"mensagem": "Meu nome é Ana", "sessao": "s2"})
    api.post("/chat", json={"mensagem": "Qual é meu nome?", "sessao": "s2"})

    textos = [m.content for m in falso.vistas]
    assert "Meu nome é Ana" in textos


def test_sessoes_nao_se_misturam(api):
    api.post("/chat", json={"mensagem": "pergunta A", "sessao": "A"})
    api.post("/chat", json={"mensagem": "pergunta B", "sessao": "B"})

    conteudos = [
        m["conteudo"]
        for m in api.get("/sessoes/A/mensagens").json()
    ]

    assert "pergunta A" in conteudos
    assert "pergunta B" not in conteudos


def test_mensagem_vazia_da_erro_422(api):
    r = api.post("/chat", json={"mensagem": "", "sessao": "x"})
    assert r.status_code == 422