from fastapi import FastAPI, Request
from pydantic import BaseModel
from src.search_engine import search_question
from openai import OpenAI
import os
import uvicorn

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Pergunta(BaseModel):
    texto: str

@app.post("/perguntar")
async def perguntar(pergunta: Pergunta):
    trechos = search_question(pergunta.texto, k=12)
    contexto = "\n\n".join([f"{i+1}. {trecho['texto']}" for i, trecho in enumerate(trechos)])

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

    # Responder usando o search_question e o modelo
    trechos = search_question(mensagem, k=12)
    contexto = "\n\n".join([f"{i+1}. {trecho['texto']}" for i, trecho in enumerate(trechos)])

    prompt = f"Responda à pergunta com base nos trechos abaixo.\n\nTrechos:\n{contexto}\n\nPergunta: {mensagem}\nResposta:"

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    resposta_final = resposta.choices[0].message.content

    # Enviar resposta de volta via Z-API
    import requests
    zapi_url = os.getenv("ZAPI_URL")  # exemplo: https://api.z-api.io/instances/{instance}/token/{token}/send-text
    payload = {
        "phone": numero,
        "message": resposta_final
    }
    requests.post(zapi_url, json=payload)

    return {"status": "mensagem enviada"}

# Para rodar localmente (opcional)
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=10000)
