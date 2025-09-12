from typing import Dict
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Produto(BaseModel):
    nome: str
    descricao: str
    preco: float
    imagem: str


class Categoria(BaseModel):
    nome: str
    produtos: Dict[str, Produto] = {}


class Cardapio(BaseModel):
    id_restaurante: UUID = Field(default_factory=uuid4)
    titulo: str
    nome_restaurante: str
    categorias: Dict[str, Categoria] = {}
