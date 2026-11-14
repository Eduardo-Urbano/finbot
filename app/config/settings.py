
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

MODELOS_PADRAO = {
    "groq": "openai/gpt-oss-120b",
    "gemini": "gemini-2.5-flash",
    "mistral": "mistral-small-latest",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # LLM
    llm_provedor: Literal["groq", "gemini", "mistral"] = "groq"
    llm_modelo: str | None = None
    groq_api_key: SecretStr | None = None
    gemini_api_key: SecretStr | None = None
    mistral_api_key: SecretStr | None = None

    # Langfuse
    langfuse_public_key: str | None = None
    langfuse_secret_key: SecretStr | None = None
    langfuse_host: str = "https://cloud.langfuse.com"

    # API
    api_url: str = "http://127.0.0.1:8000"

    # MongoDB (Aula 3)
    mongo_url: SecretStr | None = None
    mongo_banco: str = "finbot_dev"

    @property
    def modelo(self) -> str:
        return self.llm_modelo or MODELOS_PADRAO[self.llm_provedor]

    @property
    def langfuse_ativo(self) -> bool:
        segredo = (
            self.langfuse_secret_key.get_secret_value()
            if self.langfuse_secret_key
            else ""
        )
        return bool(self.langfuse_public_key and segredo)


settings = Settings()
