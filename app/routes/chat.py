from fastapi import APIRouter
from app.models.chat import ChatRequest
from app.services.grok import ask_grok

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    answer = ask_grok(request.message)

    return {
        "success": True,
        "user": request.message,
        "assistant": answer
    }