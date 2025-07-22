import os
from dotenv import load_dotenv
load_dotenv()

import faiss
import numpy as np
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

def search_question(question, k=3):
    # Caminho completo para garantir que o FAISS encontre o índice corretamente
    index_path = os.path.join("data", "nr12.index")
    metadata_path = os.path.join("data", "nr12_metadata.json")

    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Índice FAISS não encontrado em: {index_path}")
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Arquivo de metadados não encontrado em: {metadata_path}")

    index = faiss.read_index(index_path)

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    embedded_question = embed_text(question).reshape(1, -1)

    _, indices = index.search(embedded_question, k)

    trechos = []
    for idx in indices[0]:
        if idx < len(metadata):
            trechos.append(metadata[idx])
    return trechos
