import os
from search_engine import search_question
from openai import OpenAI

client = OpenAI()

def generate_answer(question):
    trechos = search_question(question, k=12)

    contexto = "\n\n".join([f"{i+1}. {trecho['text']}" for i, trecho in enumerate(trechos)])

    prompt = f"Responda à pergunta com base nos trechos abaixo.\n\nTrechos:\n{contexto}\n\nPergunta: {question}\nResposta:"

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    resposta_final = resposta.choices[0].message.content
    fontes = [trecho.get("fonte", f"Página {trecho.get('page', 'desconhecida')}") for trecho in trechos]


    return resposta_final, fontes

if __name__ == "__main__":
    question = input("Digite sua pergunta sobre a NR: ")
    resposta, fontes = generate_answer(question)

    print("\nResposta:")
    print(resposta)

    print("\nFontes:")
    for fonte in fontes:
        print("-", fonte)
