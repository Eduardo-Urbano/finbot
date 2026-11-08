from pathlib import Path

PASTA = Path(__file__).parent


def carregar(nome: str) -> str:
    return (PASTA / f"{nome}.md").read_text(encoding="utf-8").strip()
