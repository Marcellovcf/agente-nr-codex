from fastapi import FastAPI, Request
from pydantic import BaseModel
from src.search_engine import search_question

app = FastAPI()

class Consulta(BaseModel):
    pergunta: str
    k: int = 6  # número padrão de trechos retornados

@app.post("/buscar")
async def buscar(consulta: Consulta):
    try:
        trechos = search_question(consulta.pergunta, k=consulta.k)
        return {"resultados": trechos}
    except Exception as e:
        return {"erro": str(e)}
