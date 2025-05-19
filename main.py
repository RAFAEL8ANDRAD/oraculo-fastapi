from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Oráculo no comando! 🔮"}
from pydantic import BaseModel

class Nota(BaseModel):
    titulo: str
    conteudo: str

# 🧠 Rota para receber notas inteligentes
@app.post("/notas")
def criar_nota(nota: Nota):
    print(f"Nova nota: {nota.titulo} - {nota.conteudo}")
    return {"message": "Nota recebida com sucesso!", "nota": nota}
