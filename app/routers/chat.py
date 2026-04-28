from fastapi import APIRouter, Request
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, request: Request) -> ChatResponse:
    agent = request.app.state.agent
    response = agent.chat(req.message)
    return ChatResponse(response=response)
