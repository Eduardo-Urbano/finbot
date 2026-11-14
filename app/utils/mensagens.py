"""Ferramentas para lidar com o histórico de mensagens."""
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage


def conversa_limpa(
    mensagens: list[AnyMessage],
    limite: int = 10,
) -> list[AnyMessage]:
    """Só perguntas do usuário e respostas finais (sem chamadas de ferramenta).

    As últimas 'limite' mensagens bastam para manter o assunto.
    """
    limpas = [
        m for m in mensagens
        if isinstance(m, HumanMessage)
        or (isinstance(m, AIMessage) and m.content and not m.tool_calls)
    ]
    return limpas[-limite:]