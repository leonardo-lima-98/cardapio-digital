import json
from fastapi import FastAPI, HTTPException, Request
from uuid import uuid4, UUID

from fastapi.responses import RedirectResponse
from src.schemas import Cardapio, Produto
from src.utils import get_file_path, list_dir, load_json, save_json
from typing import List


app = FastAPI(title="Cardápio Digital")

# -----------------
# ROTAS
# -----------------

# Listar todos os cardápios (id + nome_restaurante)
@app.get("/")
def listar_restaurantes(request: Request):
    restaurantes = []
    for filename in list_dir():
        path = get_file_path(filename.replace(".json", ""))
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            link = f'{request.headers["host"]}/menu/{data["id_restaurante"]}'
            restaurantes.append({
                "id_restaurante": data["id_restaurante"],
                "nome_restaurante": data["nome_restaurante"],
                "link_cardapio": link
                })
    return restaurantes

# Criar novo cardápio
@app.post("/menu", response_model=Cardapio)
def criar_cardapio(titulo: str, nome_restaurante: str):
    novo_id = uuid4()
    cardapio = {
        "id_restaurante": str(novo_id),
        "titulo": titulo,
        "nome_restaurante": nome_restaurante,
        "categorias": {}
    }
    save_json(cardapio, novo_id)
    return cardapio


# Obter cardápio (via QR Code)
@app.get("/menu/{id_restaurante}", response_model=Cardapio)
def obter_cardapio(id_restaurante: UUID):
    data = load_json(id_restaurante)
    if not data:
        raise RedirectResponse("/menu")
    return data


# Adicionar categoria
@app.post("/menu/{id_restaurante}/categoria")
def adicionar_categoria(id_restaurante: UUID, categorias: str):
    data = load_json(id_restaurante)
    if not data:
        raise HTTPException(404, "Cardápio não encontrado")
    
    # Quebra a string por vírgula -> lista
    lista_categorias: List[str] = [c.strip() for c in categorias.split(",")]

    for nome in lista_categorias:
        if nome not in data["categorias"]:
            data["categorias"][nome] = {"nome": nome, "produtos": {}}

    save_json(data, id_restaurante)
    return {"categorias_adicionadas": lista_categorias}

# Adicionar produto
@app.post("/menu/{id_restaurante}/categoria/{categoria_nome}/produto", response_model=Produto)
def adicionar_produto(id_restaurante: UUID, categoria_nome: str, produto: Produto):
    data = load_json(id_restaurante)
    if not data:
        raise HTTPException(404, "Cardápio não encontrado")
    
    if categoria_nome not in data["categorias"]:
        raise HTTPException(404, "Categoria não encontrada")
    
    data["categorias"][categoria_nome]["produtos"][produto.nome] = produto.dict()
    save_json(data, id_restaurante)
    return produto


# Deletar categoria
@app.delete("/menu/{id_restaurante}/categoria/{categoria_nome}")
def deletar_categoria(id_restaurante: UUID, categoria_nome: str):
    data = load_json(id_restaurante)
    if not data:
        raise HTTPException(404, "Cardápio não encontrado")
    
    if categoria_nome not in data["categorias"]:
        raise HTTPException(404, "Categoria não encontrada")
    
    data["categorias"].pop(categoria_nome)
    save_json(data, id_restaurante)
    return {"message": f"Categoria '{categoria_nome}' removida"}


# Deletar produto
@app.delete("/menu/{id_restaurante}/categoria/{categoria_nome}/produto/{produto_nome}")
def deletar_produto(id_restaurante: UUID, categoria_nome: str, produto_nome: str):
    data = load_json(id_restaurante)
    if not data:
        raise HTTPException(404, "Cardápio não encontrado")
    
    if categoria_nome not in data["categorias"]:
        raise HTTPException(404, "Categoria não encontrada")
    
    if produto_nome not in data["categorias"][categoria_nome]["produtos"]:
        raise HTTPException(404, "Produto não encontrado")
    
    data["categorias"][categoria_nome]["produtos"].pop(produto_nome)
    save_json(data, id_restaurante)
    return {"message": f"Produto '{produto_nome}' removido"}