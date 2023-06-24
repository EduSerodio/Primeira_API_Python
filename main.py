# API - É um lugar para disponibilizar recursos e/ou funcionalidades

# Vantages de usar o FastApi :
# 1 - extremamente rápido para colocar a API no ar
# 2 - cria uma documentação automáticamente
# 3 - Gerenciamento de processos assíncronos

# Endpoints - Quais são os tipo de funcionalidades que vou disponibilizar na minha API

from fastapi import FastAPI #Estamos importando o FastAPI
from pydantic import BaseModel

app = FastAPI() #Instanciando o FastAPI

# Após isso, para colocarmos essa API criada no ar, usaremos o comando no terminal:
# uvicorn (comando pŕoprio) + nome do seu arquivo (main) + app (minha api) + --reload (comando próprio): 
# uvicorn main:app --reload
# ele vai colocar nossa api em um rota 8000, e a vantagem de ter usado o comando,
# (--reload) é que toda alteração que fizermos em nocco código ele atualizará em nossa API 

class Item(BaseModel):
    item: str
    preco_unitario: float
    quantidade: int
    

# Criando um dicionário com informações de vendas de produtos para retornar na API
vendas = {
    1: {"item": "lata", "preco_unitario": 4, "quantidade": 10},
    2: {"item": "garrafa 2L", "preco_unitario": 10, "quantidade": 50},
    3: {"item": "garrafa 750ml", "preco_unitario": 7, "quantidade": 15},
    4: {"item": "lata mini", "preco_unitario": 2, "quantidade": 5},
}

# Endpoint (GET) que vai nos retornar a quantidade de vendas que temos em nosso banco de dados
@app.get("/") #decorator é uma linha de código que atribui uma funcionalidade nova para a função que vem em seguida
def home():
    return {"Total de vendas": len(vendas), "vendas": vendas} #"len" é para saber o tamanho de um determinado item do python

# nova rota que mostre uma venda em específico pegando pelo ID
@app.get("/vendas/{id_venda}")
def pegar_venda(id_venda: int): #função pegar_venda recebendo o parametro "id_vendas" e expecificando a tipagem de dado necessária para retornar na API
    if id_venda in vendas:
        return vendas[id_venda]
    else:
        return {"Erro: Id da venda solicitado é inexistente!"}
    

# endpoint (POST) para adicionar um item novo ao dicionário de vendas
@app.post("/items")
def create_item (item: Item):
    tamanho=len(vendas) + 1 # varialvel "tamanho" que recebe um método len(vendas)+1 para adicionar um item ao dicionario
    vendas[tamanho]=item.dict()
    return vendas

# ednpoint (DELETE) para deletarmos um item de nosso dicionario (vendas) deletando pelo seu ID
@app.delete("/vendas/{id_vendas}")
def deletar_venda(id_venda: int):
    if id_venda in vendas: # bloco de condição (if) (else) para validarmos se o Id vai ou não ser deletado
        del(vendas[id_venda])
        return vendas
    else:
        return {"Erro, Id solicitado não foi encontrado!"}

# endpoint (PUT) usamos para atualizar nosso dicionário, caso queiram atualizar algum item já existente em nosso dicionario
@app.put("/vendas/{id_venda}")
def atualizar_venda(id_venda: int, body: Item):
    if id_venda in vendas:
        vendas[id_venda] = body.dict()
        return vendas
    else:
        return {"Erro ao encontrar o ID socilidado!"}


