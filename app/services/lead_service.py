import json
from datetime import datetime
from sqlalchemy.orm import Session

from app.core.normalizer import normalize
from app.gpt.llm import analyze_message
from app.core.lead_scoring import score_lead
from app.db.models import Lead, LeadAnalysis, Message


class LeadProcessingException(Exception):
    """Custom exception for lead processing errors"""
    pass


def process_lead(payload: dict, db: Session = None) -> dict:
    """
    Main orchestration function for the complete lead pipeline:
    1. Normalize (convert to standard format)
    2. Analyze (LLM extraction)
    3. Score (calculate lead value)
    4. Store (save to database)
    
    Args:
        payload: Raw webhook payload from any channel
        db: Database session (optional)
    
    Returns:
        dict: Processing result with lead data and score
    """
    
    try:
        # Step 1: Normalize the payload
        normalized = normalize(payload)
        print(f"[OK] Normalized message from {normalized['channel']}")
        
        # Step 2: Analyze message with LLM
        ai_analysis = analyze_message(normalized["message"], normalized["channel"])
        print(f"[OK] AI Analysis: Intent={ai_analysis['intent']}, Urgency={ai_analysis['urgency']}")
        
        # Step 3: Score the lead
        scoring = score_lead(ai_analysis, normalized)
        print(f"[OK] Lead Score: {scoring['total_score']} ({scoring['quality']})")
        
        # Step 4: Store to database (if session provided)
        lead_record = None
        if db:
            lead_record = _store_lead(db, normalized, ai_analysis, scoring)
            print(f"[OK] Stored to database: Lead #{lead_record.id}")
        
        # Prepare response
        result = {
            "status": "success",
            "lead_id": lead_record.id if lead_record else None,
            "channel": normalized["channel"],
            "user_id": normalized["user_id"],
            "message": normalized["message"][:100],  # Truncate for response
            "analysis": ai_analysis,
            "scoring": scoring,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return result
        
    except ValueError as e:
        raise LeadProcessingException(f"Validation error: {str(e)}")
    except Exception as e:
        raise LeadProcessingException(f"Processing error: {str(e)}")


def _store_lead(db: Session, normalized: dict, ai_analysis: dict, scoring: dict) -> Lead:
    """Store lead to database"""
    
    # Create lead record
    lead = Lead(
        channel=normalized["channel"],
        user_id=normalized["user_id"],
        user_name=normalized["user_name"] or ai_analysis.get("name"),
        user_phone=normalized["user_phone"] or ai_analysis.get("phone"),
        user_email=normalized["user_email"] or ai_analysis.get("email"),
        message=normalized["message"],
        intent=ai_analysis.get("intent"),
        urgency=ai_analysis.get("urgency"),
        category=ai_analysis.get("category"),
        contact_completeness=scoring.get("contact_completeness", 0),
        total_score=scoring.get("total_score", 0),
        quality=scoring.get("quality", "COLD"),
        score_breakdown=json.dumps(scoring.get("breakdown", {})),
        budget=ai_analysis.get("budget"),
        raw_payload=json.dumps(normalized["raw_payload"])
    )
    
    db.add(lead)
    db.flush()  # Get the ID without committing
    
    # Create analysis record
    analysis = LeadAnalysis(
        lead_id=lead.id,
        intent=ai_analysis.get("intent"),
        urgency=ai_analysis.get("urgency"),
        category=ai_analysis.get("category"),
        name=ai_analysis.get("name"),
        email=ai_analysis.get("email"),
        phone=ai_analysis.get("phone"),
        budget=ai_analysis.get("budget")
    )
    db.add(analysis)
    
    # Create message record
    message = Message(
        lead_id=lead.id,
        channel=normalized["channel"],
        user_id=normalized["user_id"],
        message_text=normalized["message"],
        raw_payload=json.dumps(normalized["raw_payload"]),
        processed_at=datetime.utcnow()
    )
    db.add(message)
    
    # Commit all records
    db.commit()
    db.refresh(lead)
    
    return lead


def get_leads(db: Session, quality: str = None, limit: int = 50):
    """
    Retrieve leads with optional filtering
    
    Args:
        db: Database session
        quality: Filter by quality (HOT, WARM, COLD)
        limit: Maximum results
    
    Returns:
        list: Lead records
    """
    query = db.query(Lead)
    
    if quality:
        query = query.filter(Lead.quality == quality.upper())
    
    return query.order_by(Lead.created_at.desc()).limit(limit).all()


def get_lead_by_id(db: Session, lead_id: int) -> Lead:
    """Get a specific lead by ID"""
    return db.query(Lead).filter(Lead.id == lead_id).first()


def mark_as_exported(db: Session, lead_id: int):
    """Mark lead as exported"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead:
        lead.exported = True
        db.commit()
        return True
    return False


def get_stats(db: Session) -> dict:
    """Get database statistics"""
    total = db.query(Lead).count()
    hot = db.query(Lead).filter(Lead.quality == "HOT").count()
    warm = db.query(Lead).filter(Lead.quality == "WARM").count()
    cold = db.query(Lead).filter(Lead.quality == "COLD").count()
    
    return {
        "total_leads": total,
        "hot_leads": hot,
        "warm_leads": warm,
        "cold_leads": cold,
        "avg_score": db.query(Lead).count() and db.query(Lead.total_score).first() or 0
    }

