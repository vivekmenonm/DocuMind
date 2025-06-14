import os
from pathlib import Path
import shutil
from fastapi import UploadFile

async def save_user_file(user_id: str, file: UploadFile) -> str:
    folder = Path(f"storage/{user_id}/uploaded_docs")
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / file.filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return str(file_path)
