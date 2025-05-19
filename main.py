from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# Rota raiz só pra teste
@app.get("/")
def read_root():
    return {"message": "Oráculo no comando! 👁‍🗨"}

# Modelo de nota
class Nota(BaseModel):
    token: str
    database_id: str
    titulo: str
    conteudo: str

# Rota que envia a nota para o Notion
@app.post("/enviar-nota")
def enviar_nota(nota: Nota):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {nota.token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": {"database_id": nota.database_id},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": nota.titulo
                        }
                    }
                ]
            },
            "Conteúdo": {
                "rich_text": [
                    {
                        "text": {
                            "content": nota.conteudo
                        }
                    }
                ]
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        return {"message": "Nota enviada com sucesso para o Notion! 🚀"}
    else:
        return {
            "message": "Erro ao enviar para o Notion.",
            "erro": response.text
        }
