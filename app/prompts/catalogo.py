
"""
Cada prompt é um arquivo .md nesta pasta (ex.: sistema.md).
Prompt é ARTEFATO, não texto solto no código.

Aula 3: o Langfuse passa a ser a "fonte da verdade".
O arquivo .md vira:
1. A semente: scripts/publicar_prompts.py envia para o Langfuse.
2. A reserva: se o Langfuse estiver fora do ar, o código usa o .md.
"""

from pathlib import Path

from app.config.settings import settings

PASTA = Path(__file__).parent


def carregar(nome: str) -> str:
    return (PASTA / f"{nome}.md").read_text(encoding="utf-8").strip()


# Nomes dos prompts locais: sistema.md -> "sistema".
def nomes_locais() -> list[str]:
    return sorted(p.stem for p in PASTA.glob("*.md"))


# No Langfuse, os prompts do projeto ganham o prefixo "finbot-".
def nome_langfuse(nome: str) -> str:
    return f"finbot-{nome}"


class PromptLocal:
    """Imita um prompt do Langfuse quando ele não está configurado ou não responde."""

    is_fallback = True
    version = "local"

    def __init__(self, texto: str):
        self.prompt = texto

    def compile(self, **variaveis) -> str:
        texto = self.prompt
        for chave, valor in variaveis.items():
            texto = texto.replace("{{" + chave + "}}", str(valor))
        return texto


def obter(nome: str):
    """Busca a versão production no Langfuse. Sem Langfuse, usa o .md local."""

    local = carregar(nome)

    if not settings.langfuse_ativo:
        return PromptLocal(local)

    try:
        from app.llm.observabilidade import cliente_langfuse

        return cliente_langfuse().get_prompt(
            nome_langfuse(nome),
            label="production",
            fallback=local,
            cache_ttl_seconds=60,
        )
    except Exception as erro:
        print(f"[prompts] Langfuse indisponível ({erro}); usando {nome}.md")
        return PromptLocal(local)
