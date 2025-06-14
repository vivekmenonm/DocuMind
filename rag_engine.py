import os
from pathlib import Path
from typing import List
from embedding_store import get_embeddings, save_faiss_index, load_faiss_index
from openai import OpenAI
from PyPDF2 import PdfReader
import docx
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text(file_path: Path) -> str:
    if file_path.suffix == ".pdf":
        reader = PdfReader(file_path)
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    elif file_path.suffix == ".docx":
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file_path.suffix == ".txt":
        return file_path.read_text()
    return ""

def generate_prompt(context: str, query: str, system_prompt: str) -> str:
    return f"""{system_prompt.strip()}

Context:
{context}

Question:
{query}

Answer:"""

async def build_user_index(user_id: str):
    doc_folder = Path(f"storage/{user_id}/uploaded_docs")
    chunks = []
    for file in doc_folder.iterdir():
        content = extract_text(file)
        for i in range(0, len(content), 500):
            chunk = content[i:i+500]
            if chunk.strip():
                chunks.append(chunk)

    embeddings = get_embeddings(chunks)
    from faiss import IndexFlatL2
    index = IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    save_faiss_index(user_id, index, chunks)

async def query_with_faiss(user_id: str, query: str, system_prompt: str) -> str:
    index, texts = load_faiss_index(user_id)
    query_embedding = get_embeddings([query])
    D, I = index.search(query_embedding, k=3)
    context = "\n\n".join([texts[i] for i in I[0]])

    prompt = generate_prompt(context, query, system_prompt)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
