from fastapi import APIRouter, UploadFile, File
import os

from app.models.rag_chat import RagQuestion

from app.services.rag import (
    read_pdf,
    split_text,
    store_chunks,
    search_pdf,
)

router = APIRouter()


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("app/uploads", exist_ok=True)

    filepath = f"app/uploads/{file.filename}"

    with open(filepath, "wb") as f:
        f.write(await file.read())

    text = read_pdf(filepath)

    chunks = split_text(text)

    store_chunks(chunks)

    return {
        "success": True,
        "filename": file.filename,
        "characters": len(text),
        "chunks": len(chunks),
        "message": "Stored successfully in ChromaDB"
    }


@router.post("/ask-pdf")
def ask_pdf(request: RagQuestion):

    answer = search_pdf(request.question)

    return {
        "question": request.question,
        "answer": answer
    }