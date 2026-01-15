from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.lead_service import process_lead, LeadProcessingException, get_leads, get_stats
from app.db.database import get_db
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class IncomingMessage(BaseModel):
    """Schema for incoming webhook payloads"""
    channel: str  # whatsapp, instagram, website
    message: Optional[str] = None
    message_text: Optional[str] = None
    text: Optional[str] = None
    user_id: Optional[str] = None
    sender_id: Optional[str] = None
    from_: Optional[str] = None
    user_name: Optional[str] = None
    name: Optional[str] = None
    sender_name: Optional[str] = None
    user_email: Optional[str] = None
    email: Optional[str] = None
    user_phone: Optional[str] = None
    phone: Optional[str] = None
    timestamp: Optional[str] = None
    visitor_id: Optional[str] = None
    contact_name: Optional[str] = None


@router.post("/webhook")
async def receive_message(payload: dict, db: Session = Depends(get_db)):
    """
    Webhook endpoint to receive messages from any channel
    
    Supports:
    - WhatsApp: /webhook?channel=whatsapp
    - Instagram: /webhook?channel=instagram
    - Website: /webhook?channel=website
    
    Returns:
    - Lead ID
    - Analysis results
    - Lead score and quality
    """
    try:
        # Process the lead through the full pipeline
        result = process_lead(payload, db)
        
        return {
            "status": "success",
            "message": "Lead received and processed",
            "data": result
        }
    
    except LeadProcessingException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Processing error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )


@router.get("/webhook/stats")
async def get_webhook_stats(db: Session = Depends(get_db)):
    """Get webhook statistics"""
    stats = get_stats(db)
    return {
        "status": "success",
        "stats": stats
    }


@router.get("/webhook/leads")
async def get_all_leads(
    quality: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get leads with optional filtering
    
    Query parameters:
    - quality: Filter by HOT, WARM, or COLD
    - limit: Maximum results (default: 50)
    """
    try:
        leads = get_leads(db, quality, limit)
        
        # Convert to dict for JSON response
        leads_data = [
            {
                "id": lead.id,
                "channel": lead.channel,
                "user_name": lead.user_name,
                "user_email": lead.user_email,
                "user_phone": lead.user_phone,
                "message": lead.message[:100],
                "intent": lead.intent,
                "urgency": lead.urgency,
                "score": lead.total_score,
                "quality": lead.quality,
                "created_at": lead.created_at.isoformat(),
                "contact_completeness": lead.contact_completeness
            }
            for lead in leads
        ]
        
        return {
            "status": "success",
            "count": len(leads_data),
            "leads": leads_data
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving leads: {str(e)}"
        )

