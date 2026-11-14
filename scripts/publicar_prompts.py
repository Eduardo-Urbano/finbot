"""Publica os prompts locais no Langfuse."""

import argparse
import sys
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_PROJETO))

from app.config.settings import settings
from app.llm.observabilidade import cliente_langfuse


PASTA_PROMPTS = Path(__file__).resolve().parents[1] / "app" / "prompts"


def publicar(forcar: bool = False) -> int:
    if not settings.langfuse_ativo:
        print("[prompts] Langfuse não configurado. Nada foi publicado.")
        return 0

    arquivos = sorted(PASTA_PROMPTS.glob("*.md"))

    if not arquivos:
        print("[prompts] Nenhum arquivo Markdown encontrado.")
        return 0

    cliente = cliente_langfuse()
    erros = 0

    for arquivo in arquivos:
        nome = f"finbot-{arquivo.stem}"
        texto = arquivo.read_text(encoding="utf-8").strip()

        if not texto:
            print(f"[prompts] {nome}: arquivo vazio, ignorado.")
            continue

        if not forcar:
            try:
                existente = cliente.get_prompt(
                    name=nome,
                    label="production",
                    type="text",
                    fallback=texto,
                    cache_ttl_seconds=0,
                )

                if not getattr(existente, "is_fallback", False):
                    print(f"[prompts] {nome}: já existe em production. Ignorado.")
                    continue

            except Exception as erro:
                print(f"[prompts] Erro ao consultar {nome}: {erro}")
                erros += 1
                continue

        try:
            publicado = cliente.create_prompt(
                name=nome,
                prompt=texto,
                labels=["production"],
                type="text",
                commit_message="Publicado pelo FinBot",
            )

            versao = getattr(publicado, "version", "não informada")
            print(f"[prompts] {nome}: publicado. Versão {versao}.")

        except Exception as erro:
            print(f"[prompts] Erro ao publicar {nome}: {erro}")
            erros += 1

    print(f"\nPublicação finalizada. Erros: {erros}.")
    return 1 if erros else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Publica os prompts locais no Langfuse."
    )
    parser.add_argument(
        "--forcar",
        action="store_true",
        help="Publica uma nova versão mesmo que já exista em production.",
    )
    argumentos = parser.parse_args()

    raise SystemExit(publicar(forcar=argumentos.forcar))
