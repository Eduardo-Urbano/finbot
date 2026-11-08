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

    llm_provedor: Literal["groq", "gemini", "mistral"] = "groq"
    llm_modelo: str | None = None
    groq_api_key: SecretStr | None = None
    gemini_api_key: SecretStr | None = None
    mistral_api_key: SecretStr | None = None

    @property
    def modelo(self) -> str:
        return self.llm_modelo or MODELOS_PADRAO[self.llm_provedor]


settings = Settings()
