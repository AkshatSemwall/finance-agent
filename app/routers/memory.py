from fastapi import APIRouter, Request

router = APIRouter()

@router.delete("/memory")
async def clear_memory(request: Request) -> dict:
    agent = request.app.state.agent
    agent.memory_manager.clear()
    return {"message": "Memory cleared successfully"}