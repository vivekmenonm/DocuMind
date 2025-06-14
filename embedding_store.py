import faiss
import os
import pickle
from typing import List
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embeddings(texts: List[str]) -> np.ndarray:
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    return np.array([e.embedding for e in response.data])

def save_faiss_index(user_id: str, index, texts: List[str]):
    folder = f"storage/{user_id}/faiss_index"
    os.makedirs(folder, exist_ok=True)
    faiss.write_index(index, os.path.join(folder, "index.bin"))
    with open(os.path.join(folder, "texts.pkl"), "wb") as f:
        pickle.dump(texts, f)

def load_faiss_index(user_id: str):
    folder = f"storage/{user_id}/faiss_index"
    index = faiss.read_index(os.path.join(folder, "index.bin"))
    with open(os.path.join(folder, "texts.pkl"), "rb") as f:
        texts = pickle.load(f)
    return index, texts
