from langchain_core.messages import HumanMessage, SystemMessage

from app.config.settings import settings
from app.llm.fabrica import criar_modelo
from app.prompts import catalogo


modelo = criar_modelo()
historico = [SystemMessage(catalogo.carregar("sistema"))]

print(
    f"FinBot ({settings.llm_provedor} / {settings.modelo}) "
    "- digite 'sair' para encerrar\n"
)

while True:
    pergunta = input("Você: ").strip()

    if pergunta.lower() in ("sair", "exit"):
        break

    if not pergunta:
        continue

    historico.append(HumanMessage(pergunta))
    resposta = modelo.invoke(historico)
    historico.append(resposta)

    tokens = resposta.usage_metadata or {}

    print(
        f"\nFinBot: {resposta.content}\n"
        f"   [tokens: entrada={tokens.get('input_tokens')} "
        f"saída={tokens.get('output_tokens')}]\n"
    )