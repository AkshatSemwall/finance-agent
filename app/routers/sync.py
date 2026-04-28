from fastapi import APIRouter, Request
from pydantic import BaseModel

class SyncRequest(BaseModel):
    csv_path: str = "data/sample.csv"

router = APIRouter()

@router.post("/sync")
async def sync_transactions(req: SyncRequest, request: Request) -> dict:
    csv_importer = request.app.state.csv_importer
    csv_importer.import_csv(req.csv_path)
    return {"message": "Transactions synced successfully"}