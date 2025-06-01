from fastapi import FastAPI, Request
from notion_client import Client
from datetime import datetime
import os

app = FastAPI()

# 🔐 Pegue da variável de ambiente (Render segura) ou hardcoded (não recomendado)
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "coloque_seu_token_aqui")
DATABASE_ID = os.getenv("NOTION_DB_ID", "coloque_seu_database_id_aqui")

notion = Client(auth=NOTION_TOKEN)

@app.post("/registrar-trade")
async def registrar_trade(request: Request):
    data = await request.json()

    par = data.get("par", "Desconhecido")
    direcao = data.get("direcao", "long")
    preco = data.get("preco_entrada", 0.0)
    sl = data.get("stop_loss", 0.0)
    tp = data.get("take_profit", 0.0)
    estrategia = data.get("estrategia", "Não informado")
    resultado = data.get("resultado", "pendente")
    timestamp = datetime.now().isoformat()

    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "par": {"title": [{"text": {"content": par}}]},
            "direcao": {"select": {"name": direcao}},
            "preco_entrada": {"number": preco},
            "stop_loss": {"number": sl},
            "take_profit": {"number": tp},
            "estrategia": {"rich_text": [{"text": {"content": estrategia}}]},
            "timestamp": {"date": {"start": timestamp}},
            "resultado": {"select": {"name": resultado}},
        }
    )

    return {"status": "registrado", "notion_id": response["id"]}
