from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class LeadQualityEnum(str, enum.Enum):
    HOT = "HOT"
    WARM = "WARM"
    COLD = "COLD"


class Lead(Base):
    """Core Lead model"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic info
    channel = Column(String(50), index=True)
    user_id = Column(String(255), index=True)
    user_name = Column(String(255), nullable=True)
    user_phone = Column(String(255), nullable=True)
    user_email = Column(String(255), nullable=True)
    
    # Message content
    message = Column(Text, nullable=False)
    
    # AI Analysis
    intent = Column(String(50), default="inquiry")
    urgency = Column(String(50), default="low")
    category = Column(String(50), default="general")
    
    # Contact completeness
    contact_completeness = Column(Integer, default=0)
    
    # Scoring
    total_score = Column(Float, default=0)
    quality = Column(String(10), default="COLD")
    score_breakdown = Column(Text)  # JSON string
    
    # Budget (if mentioned)
    budget = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    processed = Column(Boolean, default=True)
    exported = Column(Boolean, default=False)
    
    # Raw data
    raw_payload = Column(Text)  # JSON string
    
    def __repr__(self):
        return f"<Lead(id={self.id}, channel={self.channel}, quality={self.quality}, score={self.total_score})>"


class LeadAnalysis(Base):
    """Detailed analysis records"""
    __tablename__ = "lead_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, index=True)
    
    # Full analysis
    intent = Column(String(50))
    urgency = Column(String(50))
    category = Column(String(50))
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    budget = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<LeadAnalysis(lead_id={self.lead_id}, intent={self.intent})>"


class Message(Base):
    """Raw messages for audit trail"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, index=True)
    
    channel = Column(String(50))
    user_id = Column(String(255))
    message_text = Column(Text)
    
    # Source
    raw_payload = Column(Text)  # JSON string
    
    # Timestamps
    received_at = Column(DateTime, default=datetime.utcnow, index=True)
    processed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Message(id={self.id}, channel={self.channel}, user_id={self.user_id})>"
