```markdown
# 🔐 DocuMind – Secure Retrieval-Augmented Generation API

RAGGuard is a secure, user-isolated Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **FAISS**, and **OpenAI**. It allows authenticated users to upload documents, build vector indexes (FAISS), and ask natural language questions using OpenAI's GPT models – all protected with **JWT authentication**.

---

## 🚀 Features

- ✅ JWT-based user authentication
- ✅ Document upload support (PDF, DOCX, TXT)
- ✅ FAISS vector index per user
- ✅ Contextual Q&A via OpenAI GPT (RAG)
- ✅ Swagger UI (`/docs`) with secure Bearer token auth
- ✅ Customizable prompt templates
- 🔐 User isolation: only access your own files and embeddings

---

## 📁 Directory Structure

```

rag\_guard/
├── main.py                # FastAPI app entry point
├── auth.py                # JWT config and secret loading
├── file\_handler.py        # Upload and save user files
├── rag\_engine.py          # Indexing and GPT-based querying
├── embedding\_store.py     # FAISS save/load + embeddings
├── storage/               # User data (organized per user\_id)
│   └── user\_xyz/
├── .env                   # Secrets like API keys
├── requirements.txt
├── README.md

````

---

## 🔧 Requirements

- Python 3.8+
- OpenAI API key
- Virtual environment

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/ragguard.git
cd ragguard
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
````

---

## 🔐 Environment Setup

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key_here
JWT_SECRET_KEY=your_secret_key_here
```

> 💡 Generate a strong secret using:
> `python -c "import secrets; print(secrets.token_urlsafe(32))"`

---

## 🏃 Run the Server

```bash
uvicorn main:app --reload
```

Then open:
🔗 [http://localhost:8000/docs](http://localhost:8000/docs) — Swagger UI

---

## 🧪 Example Workflow (Swagger)

1. 🔐 **POST `/login/`**

   * username: `demo`
   * password: `demo123`

2. ✅ Copy the returned token → click **"Authorize"** → paste:

   ```
   Bearer <your_token>
   ```

3. 📁 **POST `/upload/`** — Upload PDF, DOCX, or TXT file

4. 🤖 **POST `/query/`** — Ask a question (optional: customize `system_prompt`)

---

## 🔍 Prompt Customization

The `/query/` endpoint accepts an optional `system_prompt` field to guide the LLM response tone and style.

Examples:

```text
You are a lawyer. Answer with legal precision.
Explain in plain English for a 10-year-old.
Summarize in bullet points.
```

---

## 🛡️ Security

* All endpoints (except `/login`) require JWT Bearer token.
* Each user's documents and vector index are stored separately.
* Prompt inputs are sanitized by OpenAI, but additional checks are encouraged for production.

---

## 📚 Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [OpenAI API](https://platform.openai.com/)
* [fastapi-jwt-auth](https://github.com/IndominusByte/fastapi-jwt-auth)

---

## 📌 TODO

* [ ] Add user registration
* [ ] Support multi-language documents
* [ ] Stream LLM responses
* [ ] Integrate with Chroma or Pinecone
* [ ] Web frontend (optional)

---

## 📝 License

MIT License – Use, modify, and share freely.

---

## 🤖 Made with AI and FastAPI ❤️

```

---

Would you like a `Dockerfile` or GitHub Actions workflow to package and deploy this next?
```
