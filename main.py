from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from file_handler import save_user_file
from rag_engine import build_user_index, query_with_faiss
from auth import Settings
from fastapi.openapi.utils import get_openapi

app = FastAPI()

@app.exception_handler(AuthJWTException)
def auth_exception_handler(request, exc):
    return JSONResponse(status_code=401, content={"detail": exc.message})

@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...), Authorize: AuthJWT = Depends()):
    if username != "demo" or password != "demo123":
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})
    user_id = f"user_{username}"
    access_token = Authorize.create_access_token(subject=user_id)
    return {"access_token": access_token}

@app.post("/upload/")
async def upload(file: UploadFile = File(...), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    path = await save_user_file(user_id, file)
    await build_user_index(user_id)
    return {"message": "File uploaded", "path": path}

@app.post("/query/")
async def query_document(
    query: str = Form(...),
    system_prompt: str = Form(default="You are a helpful assistant. Use the context to answer the question accurately."),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    answer = await query_with_faiss(user_id, query, system_prompt)
    return {"answer": answer}

# 🔐 Add Bearer auth to Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="RAG API with JWT",
        version="1.0.0",
        description="Upload and query documents using FAISS + OpenAI",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
