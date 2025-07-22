from fastapi import FastAPI, Request
from pydantic import BaseModel
from src.search_engine import search_question
from openai import OpenAI
import os
import requests

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Pergunta(BaseModel):
    texto: str

@app.post("/perguntar")
async def perguntar(pergunta: Pergunta):
    trechos = search_question(pergunta.texto, k=12)
    contexto = "\n\n".join([f"{i+1}. {trecho['content']}" for i, trecho in enumerate(trechos)])

    prompt = f"Responda à pergunta com base nos trechos abaixo.\n\nTrechos:\n{contexto}\n\nPergunta: {pergunta.texto}\nResposta:"

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    resposta_final = resposta.choices[0].message.content
    return {"resposta": resposta_final}

@app.post("/webhook")
async def receber_whatsapp(request: Request):
    body = await request.json()

    try:
        mensagem = body["message"]["body"]
        numero = body["message"]["from"]
    except KeyError:
        return {"erro": "Formato inesperado"}

    print(f"📩 Mensagem recebida de {numero}: {mensagem}")

    trechos = search_question(mensagem, k=12)
    contexto = "\n\n".join([f"{i+1}. {trecho['content']}" for i, trecho in enumerate(trechos)])

    prompt = f"Responda à pergunta com base nos trechos abaixo.\n\nTrechos:\n{contexto}\n\nPergunta: {mensagem}\nResposta:"

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    resposta_final = resposta.choices[0].message.content

    zapi_url = os.getenv("ZAPI_URL")
    payload = {
        "phone": numero,
        "message": resposta_final
    }

    try:
        zap_resp = requests.post(zapi_url, json=payload)
        print(f"✅ Resposta enviada para {numero}: {resposta_final}")
        print(f"📦 Z-API Status: {zap_resp.status_code}, Body: {zap_resp.text}")
    except Exception as e:
        print(f"❌ Erro ao enviar resposta via ZAPI: {e}")

    return {"status": "mensagem enviada"}
