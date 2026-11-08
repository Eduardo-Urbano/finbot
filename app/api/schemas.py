from pydantic import BaseModel, Field


class Pergunta(BaseModel):
    mensagem: str = Field(min_length=1, examples=["O que é CDI?"])
    sessao: str = Field(examples=["sessao-123"])
    usuario: str = "anonimo"


class Resposta(BaseModel):
    resposta: str


class Mensagem(BaseModel):
    papel: str
    conteudo: str