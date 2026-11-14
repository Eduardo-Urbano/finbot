
import os
import uuid
from urllib.parse import quote

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


# Estado inicial da aplicação
if "sessao" not in st.session_state:
    st.session_state.sessao = str(uuid.uuid4())[:8]
    st.session_state.mensagens = []

if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = "aluno1"

if "usuario_input" not in st.session_state:
    st.session_state.usuario_input = "aluno1"

if "conversa_selecionada" not in st.session_state:
    st.session_state.conversa_selecionada = None


# Barra lateral
with st.sidebar:
    st.header("👤 Usuário")

    usuario = st.text_input(
        "Identificador",
        key="usuario_input",
        help="Use sempre o mesmo identificador para recuperar seu perfil e conversas.",
    ).strip()

    if not usuario:
        st.warning("Informe um identificador de usuário.")
        st.stop()

    # Ao trocar de usuário, inicia uma sessão e carrega seu perfil.
    if usuario != st.session_state.usuario_atual:
        st.session_state.usuario_atual = usuario
        st.session_state.sessao = str(uuid.uuid4())[:8]
        st.session_state.mensagens = []
        st.session_state.conversa_selecionada = None

        try:
            perfil = api("GET", f"/usuarios/{quote(usuario, safe='')}/perfil")
            st.session_state.perfil_nome = perfil.get("nome", "")
            st.session_state.perfil_objetivo = perfil.get("objetivo", "")
            st.session_state.perfil_experiencia = perfil.get("experiencia", "")
        except Exception as erro:
            st.error(f"Erro ao carregar perfil: {erro}")

    st.divider()
    st.subheader("Meu perfil")

    with st.form("form_perfil"):
        nome = st.text_input(
            "Nome",
            key="perfil_nome",
        )
        objetivo = st.text_input(
            "Objetivo financeiro",
            key="perfil_objetivo",
        )
        experiencia = st.text_input(
            "Experiência com investimentos",
            key="perfil_experiencia",
        )

        salvar = st.form_submit_button("Salvar perfil")

        if salvar:
            try:
                api(
                    "PUT",
                    f"/usuarios/{quote(usuario, safe='')}/perfil",
                    json={
                        "nome": nome,
                        "objetivo": objetivo,
                        "experiencia": experiencia,
                    },
                )
                st.success("Perfil salvo!")
            except Exception as erro:
                st.error(f"Erro ao salvar perfil: {erro}")

    st.divider()
    st.subheader("💬 Conversas")

    if st.button("＋ Nova conversa", use_container_width=True):
        st.session_state.sessao = str(uuid.uuid4())[:8]
        st.session_state.mensagens = []
        st.session_state.conversa_selecionada = None
        st.rerun()

    try:
        conversas = api(
            "GET",
            f"/usuarios/{quote(usuario, safe='')}/conversas",
        )

        titulos = {
            conversa["sessao"]: conversa.get("titulo", "Nova conversa")
            for conversa in conversas
        }

        opcoes = [None] + list(titulos.keys())

        selecionada = st.selectbox(
            "Histórico",
            options=opcoes,
            format_func=lambda sessao: (
                "Conversa atual" if sessao is None else titulos[sessao]
            ),
            key="conversa_selecionada",
        )

        if selecionada and selecionada != st.session_state.sessao:
            historico = api(
                "GET",
                f"/sessoes/{quote(selecionada, safe='')}/mensagens",
            )
            st.session_state.sessao = selecionada
            st.session_state.mensagens = historico
            st.rerun()

    except Exception as erro:
        st.error(f"Erro ao carregar conversas: {erro}")


def mostrar(mensagem: dict):
    with st.chat_message(mensagem["papel"]):
        st.markdown(mensagem["conteudo"])


# Exibe o histórico da conversa atual
for mensagem in st.session_state.mensagens:
    mostrar(mensagem)


# Entrada de novas mensagens
if pergunta := st.chat_input(
    "Pergunte sobre CDI, Tesouro, FIIs, ações..."
):
    mensagem_usuario = {
        "papel": "user",
        "conteudo": pergunta,
    }

    st.session_state.mensagens.append(mensagem_usuario)
    mostrar(mensagem_usuario)

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
    st.rerun()