from fastapi import FastAPI, Request
from pydantic import BaseModel
from search_engine import search_question
from openai import OpenAI
import os

client = OpenAI()

app = FastAPI()

class Pergunta(BaseModel):
    texto: str

@app.post("/perguntar")
def responder(pergunta: Pergunta):
    trechos = search_question(pergunta.texto, k=10)
    contexto = "\n\n".join([f"{i+1}. {t.get('text') or t.get('texto') or t.get('content')}" for i, t in enumerate(trechos)])

    prompt = f"Responda à pergunta com base nos trechos abaixo.\n\nTrechos:\n{contexto}\n\nPergunta: {pergunta.texto}\nResposta:"

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    texto_resposta = resposta.choices[0].message.content
    fontes = [t.get("fonte") or f"Página {t.get('page')}" for t in trechos]

    return {
        "resposta": texto_resposta,
        "fontes": fontes
    }
