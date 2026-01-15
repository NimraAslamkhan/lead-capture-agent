from app.config import HOT_LEAD_THRESHOLD, WARM_LEAD_THRESHOLD
import re


def score_lead(ai_analysis, normalized_data=None):
    """
    Calculate lead score based on AI analysis and normalized data
    
    Scoring rules:
    - Intent: buy (+50), question (+20), complaint (0), inquiry (+10)
    - Urgency: high (+30), medium (+15), low (0)
    - Contact info: each piece (+10) - name, email, phone
    - Category: premium (+25), enterprise (+30), support (-10), general (0)
    - Has contact details: (+10 bonus if 2+ fields)
    
    Threshold:
    - ≥60: HOT lead 🔥
    - 40-59: WARM lead 🔆
    - <40: COLD lead ❄️
    """
    
    score = 0
    breakdown = {}
    
    # 1. Intent scoring
    intent_scores = {
        "buy": 50,
        "question": 20,
        "inquiry": 10,
        "complaint": 0
    }
    intent = ai_analysis.get("intent", "inquiry").lower()
    intent_points = intent_scores.get(intent, 10)
    score += intent_points
    breakdown["intent"] = intent_points
    
    # 2. Urgency scoring
    urgency_scores = {
        "high": 30,
        "medium": 15,
        "low": 0
    }
    urgency = ai_analysis.get("urgency", "low").lower()
    urgency_points = urgency_scores.get(urgency, 0)
    score += urgency_points
    breakdown["urgency"] = urgency_points
    
    # 3. Category scoring
    category_scores = {
        "enterprise": 30,
        "premium": 25,
        "general": 0,
        "support": -10
    }
    category = ai_analysis.get("category", "general").lower()
    category_points = category_scores.get(category, 0)
    score += category_points
    breakdown["category"] = category_points
    
    # 4. Contact info scoring
    contact_points = 0
    contact_count = 0
    
    if ai_analysis.get("name", "").strip():
        contact_points += 10
        contact_count += 1
    
    if ai_analysis.get("email", "").strip() and is_valid_email(ai_analysis.get("email", "")):
        contact_points += 10
        contact_count += 1
    
    if ai_analysis.get("phone", "").strip() and is_valid_phone(ai_analysis.get("phone", "")):
        contact_points += 10
        contact_count += 1
    
    # Bonus for multiple contact fields
    if contact_count >= 2:
        contact_points += 10
    
    score += contact_points
    breakdown["contact_info"] = contact_points
    
    # 5. Normalized data bonus (if available)
    data_bonus = 0
    if normalized_data:
        if normalized_data.get("user_phone"):
            data_bonus += 5
        if normalized_data.get("user_email"):
            data_bonus += 5
    
    score += data_bonus
    breakdown["data_source_bonus"] = data_bonus
    
    # Determine lead quality
    quality = determine_quality(score)
    
    return {
        "total_score": max(0, score),  # Don't allow negative scores
        "quality": quality,
        "breakdown": breakdown,
        "contact_completeness": contact_count
    }


def determine_quality(score):
    """Determine lead quality based on score"""
    if score >= HOT_LEAD_THRESHOLD:
        return "HOT"
    elif score >= WARM_LEAD_THRESHOLD:
        return "WARM"
    else:
        return "COLD"


def is_valid_email(email):
    """Simple email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None


def is_valid_phone(phone):
    """Simple phone validation (10+ digits)"""
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10
