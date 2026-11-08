from langchain_core.language_models import BaseChatModel

from app.config.settings import settings


def _chave(segredo) -> str:
    if segredo is None or not segredo.get_secret_value():
        raise RuntimeError(
            f"Defina a chave do provedor '{settings.llm_provedor}' no arquivo .env"
        )
    return segredo.get_secret_value()


def criar_modelo(temperatura: float = 0.3) -> BaseChatModel:
    if settings.llm_provedor == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(
            model=settings.modelo,
            temperature=temperatura,
            api_key=_chave(settings.groq_api_key),
        )

    if settings.llm_provedor == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=settings.modelo,
            temperature=temperatura,
            google_api_key=_chave(settings.gemini_api_key),
        )

    if settings.llm_provedor == "mistral":
        from langchain_mistralai import ChatMistralAI

        return ChatMistralAI(
            model=settings.modelo,
            temperature=temperatura,
            api_key=_chave(settings.mistral_api_key),
        )

    raise ValueError(f"Provedor desconhecido: {settings.llm_provedor}")
