from fastapi import FastAPI, Request
import requests
import datetime

app = FastAPI()

NOTION_TOKEN = "seu_token_aqui"
NOTION_DATABASE_ID = "seu_database_id_aqui"
NOTION_API_URL = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def criar_trade_notion(data):
    body = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Data": {
                "date": {
                    "start": datetime.datetime.utcnow().date().isoformat()
                }
            },
            "Par Operado": {
                "title": [{
                    "text": {"content": data["par"]}
                }]
            },
            "Entrada": {
                "number": float(data["preco"])
            },
            "Horário do Trade": {
                "rich_text": [{
                    "text": {"content": data["hora"]}
                }]
            },
            "Resultado": {
                "multi_select": [{
                    "name": "🔮 Pendente"
                }]
            }
        }
    }

    response = requests.post(NOTION_API_URL, headers=headers, json=body)
    return response.status_code

@app.post("/webhook")
async def receber_sinal(request: Request):
    payload = await request.json()
    print("Recebido:", payload)
    status = criar_trade_notion(payload)
    return {"status": "enviado", "notion_status": status}
