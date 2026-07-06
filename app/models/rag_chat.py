from pydantic import BaseModel


class RagQuestion(BaseModel):
    question: str