import pandas as pd
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.lead_service import get_leads, mark_as_exported
from app.config import EXPORT_PATH


def export_to_excel(db: Session, filename: str = None, quality: str = None) -> str:
    """
    Export leads to Excel file
    
    Args:
        db: Database session
        filename: Output filename (default: leads_YYYYMMDD_HHMMSS.xlsx)
        quality: Filter by quality (HOT, WARM, COLD) or None for all
    
    Returns:
        str: Path to exported file
    """
    
    # Create export directory if it doesn't exist
    os.makedirs(EXPORT_PATH, exist_ok=True)
    
    # Get leads
    leads = get_leads(db, quality=quality, limit=10000)
    
    if not leads:
        raise ValueError("No leads found to export")
    
    # Convert to DataFrame
    data = []
    for lead in leads:
        data.append({
            "ID": lead.id,
            "Channel": lead.channel,
            "Name": lead.user_name or "",
            "Email": lead.user_email or "",
            "Phone": lead.user_phone or "",
            "Message": lead.message,
            "Intent": lead.intent,
            "Urgency": lead.urgency,
            "Category": lead.category,
            "Lead Score": lead.total_score,
            "Quality": lead.quality,
            "Contact Completeness": lead.contact_completeness,
            "Budget": lead.budget or "",
            "Created At": lead.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "User ID": lead.user_id
        })
    
    df = pd.DataFrame(data)
    
    # Generate filename
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        quality_suffix = f"_{quality}" if quality else ""
        filename = f"leads_{timestamp}{quality_suffix}.xlsx"
    
    filepath = os.path.join(EXPORT_PATH, filename)
    
    # Export to Excel
    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Leads", index=False)
        
        # Add summary sheet
        summary_data = {
            "Metric": ["Total Leads", "Hot Leads", "Warm Leads", "Cold Leads", "Export Date"],
            "Value": [
                len(df),
                len(df[df["Quality"] == "HOT"]),
                len(df[df["Quality"] == "WARM"]),
                len(df[df["Quality"] == "COLD"]),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
    
    # Mark leads as exported
    for lead in leads:
        mark_as_exported(db, lead.id)
    
    print(f"[OK] Exported {len(leads)} leads to {filepath}")
    return filepath


def export_hot_leads(db: Session) -> str:
    """Quick export of HOT leads only"""
    return export_to_excel(db, quality="HOT", filename="hot_leads.xlsx")


def export_warm_leads(db: Session) -> str:
    """Quick export of WARM leads only"""
    return export_to_excel(db, quality="WARM", filename="warm_leads.xlsx")


def export_all_leads(db: Session) -> str:
    """Export all leads"""
    return export_to_excel(db, filename="all_leads.xlsx")


def get_export_stats(db: Session) -> dict:
    """Get statistics about exported leads"""
    leads = db.query(Lead).filter(Lead.exported == True).all()
    
    return {
        "total_exported": len(leads),
        "by_quality": {
            "hot": len([l for l in leads if l.quality == "HOT"]),
            "warm": len([l for l in leads if l.quality == "WARM"]),
            "cold": len([l for l in leads if l.quality == "COLD"])
        },
        "by_channel": {
            "whatsapp": len([l for l in leads if l.channel == "whatsapp"]),
            "instagram": len([l for l in leads if l.channel == "instagram"]),
            "website": len([l for l in leads if l.channel == "website"])
        }
    }


# Import Lead model for queries
from app.db.models import Lead
