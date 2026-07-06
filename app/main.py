from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.health import router as health_router
from app.routes.rag import router as rag_router

app = FastAPI(
    title="AI Agent API",
    version="2.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Agent"
    }


app.include_router(chat_router)
app.include_router(health_router)
app.include_router(rag_router)