import json
import faiss
import numpy as np
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    with open("data/nr12_text.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    embeddings = []
    metadata = []

    print("🔄 Gerando embeddings...")

    for i, item in enumerate(data):
        try:
            emb = get_embedding(item["text"])
            embeddings.append(emb)
            metadata.append(item)
            print(f"✅ Página {item['page']} indexada")
            time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ Erro na página {item['page']}: {e}")

    if embeddings:
        index = faiss.IndexFlatL2(len(embeddings[0]))
        index.add(np.array(embeddings).astype("float32"))
        faiss.write_index(index, "data/nr12.index")
        print("📌 Índice vetorial salvo em data/nr12.index")

        with open("data/nr12_metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print("📌 Metadados salvos em data/nr12_metadata.json")
    else:
        print("❌ Nenhum embedding foi gerado. Verifique a chave ou o limite da API.")

