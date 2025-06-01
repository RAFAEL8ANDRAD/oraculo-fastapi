from fastapi import FastAPI, Request
from notion_client import Client
from datetime import datetime

app = FastAPI()

# Aqui você cola seu token secreto do Notion
notion = Client(auth="seu_token_secreto_notion")

# Aqui você cola o ID da sua database do Notion
database_id = "seu_database_id_aqui"

@app.post("/webhook")
async def receber_trade(request: Request):
    payload = await request.json()

    ativo = payload.get("ativo")
    preco = payload.get("preco")
    direcao = payload.get("direcao")
    data = payload.get("data")

    # Converte a data do TradingView (em milissegundos) para formato de data do Notion
    data_formatada = datetime.utcfromtimestamp(int(data) / 1000).isoformat()

    # Envia os dados para o Notion
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Ativo": {"title": [{"text": {"content": ativo}}]},
            "Preço": {"number": float(preco)},
            "Direção": {"select": {"name": direcao}},
            "Data": {"date": {"start": data_formatada}},
            "Status": {"rich_text": [{"text": {"content": "Pendente"}}]}
        }
    )

    return {"status": "registrado com sucesso no Notion"}
