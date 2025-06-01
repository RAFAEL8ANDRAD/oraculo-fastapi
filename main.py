from fastapi import FastAPI, Request
from notion_client import Client
from datetime import datetime

app = FastAPI()

notion = Client(auth="SEU_TOKEN_DO_NOTION")
database_id = "SEU_DATABASE_ID"

@app.post("/webhook")
async def receber_trade(request: Request):
    payload = await request.json()

    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "📈 Par Operado": {"title": [{"text": {"content": payload["par"]}}]},
            "📍 Entrada": {"number": payload["entrada"]},
            "🎯 Alvo (TP)": {"number": payload["tp"]},
            "🛑 Stop (SL)": {"number": payload["sl"]},
            "🎥 Print ou Link do Gráfico (TradingView)": {"url": payload["grafico"]},
            "📊 Motivo da Entrada": {
                "multi_select": [{"name": motivo} for motivo in payload["motivos"]]
            },
            "💡 Confirmações adicionais": {
                "multi_select": [{"name": item} for item in payload["confirmacoes"]]
            },
            "🧠 Psicologia na entrada": {
                "rich_text": [{"text": {"content": payload["psicologia"]}}]
            },
            "📌 Resultado": {"select": {"name": payload["resultado"]}},
            "💬 Observações pós-trade": {
                "rich_text": [{"text": {"content": payload["observacoes"]}}]
            },
            "📅 Data": {"date": {"start": payload["data"]}}
        }
    )

    return {"status": "Trade registrado no Notion"}
