from fastapi import APIRouter, Request
from typing import List, Dict, Any

router = APIRouter()

@router.get("/transactions")
async def get_transactions(request: Request) -> List[Dict[str, Any]]:
    csv_importer = request.app.state.csv_importer
    return csv_importer.fetch()
