import os
import uuid

import requests
import streamlit as st


def config(nome: str, padrao: str) -> str:
    try:
        return os.getenv(nome) or st.secrets.get(nome, padrao)
    except Exception:
        return padrao


API_URL = config("API_URL", "http://127.0.0.1:8000").rstrip("/")
TEMPO_LIMITE = 120


def api(metodo: str, caminho: str, **kwargs):
    resposta = requests.request(
        metodo,
        f"{API_URL}{caminho}",
        timeout=TEMPO_LIMITE,
        **kwargs,
    )
    resposta.raise_for_status()
    return resposta.json()


st.set_page_config(page_title="FinBot", page_icon="💬")
st.title("💬 FinBot")
st.caption(
    "Chat educacional sobre investimentos — "
    "não é recomendação de investimento."
)

if "sessao" not in st.session_state:
    st.session_state.sessao = str(uuid.uuid4())[:8]
    st.session_state.mensagens = []

usuario = "aluno1"


def mostrar(m: dict):
    with st.chat_message(m["papel"]):
        st.markdown(m["conteudo"])


for mensagem in st.session_state.mensagens:
    mostrar(mensagem)


if pergunta := st.chat_input(
    "Pergunte sobre CDI, Tesouro, FIIs, ações..."
):
    st.session_state.mensagens.append(
        {"papel": "user", "conteudo": pergunta}
    )
    mostrar(st.session_state.mensagens[-1])

    with st.spinner("Pensando..."):
        try:
            resposta = api(
                "POST",
                "/chat",
                json={
                    "mensagem": pergunta,
                    "sessao": st.session_state.sessao,
                    "usuario": usuario,
                },
            )

            mensagem = {
                "papel": "assistant",
                "conteudo": resposta["resposta"],
                "agente": resposta.get("agente"),
                "fontes": resposta.get("fontes", []),
            }

        except Exception as erro:
            mensagem = {
                "papel": "assistant",
                "conteudo": f"⚠️ Erro ao falar com a API: {erro}",
            }

    st.session_state.mensagens.append(mensagem)
    mostrar(mensagem)