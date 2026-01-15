from fastapi import APIRouter
from app.services.lead_service import process_lead

router = APIRouter()

@router.post("/webhook")
async def receive_message(payload: dict):
    process_lead(payload)
    return {"message": "received"}
