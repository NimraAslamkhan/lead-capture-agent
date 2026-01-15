from datetime import datetime

def normalize(payload):
    """
    Convert different platform payloads into standard format
    Supports: WhatsApp, Instagram, Website chat
    
    Standard format:
    {
        "channel": str,
        "message": str,
        "user_id": str,
        "user_name": str,
        "user_phone": str,
        "user_email": str,
        "timestamp": datetime,
        "raw_payload": dict
    }
    """
    
    if not payload or not isinstance(payload, dict):
        raise ValueError("Invalid payload")
    
    channel = payload.get("channel", "unknown").lower()
    
    if channel == "whatsapp":
        return _normalize_whatsapp(payload)
    elif channel == "instagram":
        return _normalize_instagram(payload)
    elif channel == "website":
        return _normalize_website(payload)
    else:
        return _normalize_generic(payload)


def _normalize_whatsapp(payload):
    """Normalize WhatsApp webhook payload"""
    return {
        "channel": "whatsapp",
        "message": payload.get("message_text", "").strip(),
        "user_id": payload.get("from", ""),
        "user_name": payload.get("contact_name", ""),
        "user_phone": payload.get("from", ""),
        "user_email": "",
        "timestamp": datetime.fromisoformat(payload.get("timestamp", datetime.now().isoformat())),
        "raw_payload": payload
    }


def _normalize_instagram(payload):
    """Normalize Instagram DM payload"""
    return {
        "channel": "instagram",
        "message": payload.get("text", "").strip(),
        "user_id": payload.get("sender_id", ""),
        "user_name": payload.get("sender_name", ""),
        "user_phone": "",
        "user_email": payload.get("sender_email", ""),
        "timestamp": datetime.fromisoformat(payload.get("timestamp", datetime.now().isoformat())),
        "raw_payload": payload
    }


def _normalize_website(payload):
    """Normalize Website chat payload"""
    return {
        "channel": "website",
        "message": payload.get("chat", "").strip() or payload.get("message", "").strip(),
        "user_id": payload.get("visitor_id", ""),
        "user_name": payload.get("name", ""),
        "user_phone": payload.get("phone", ""),
        "user_email": payload.get("email", ""),
        "timestamp": datetime.fromisoformat(payload.get("timestamp", datetime.now().isoformat())),
        "raw_payload": payload
    }


def _normalize_generic(payload):
    """Normalize generic payload (flexible structure)"""
    return {
        "channel": payload.get("channel", "unknown"),
        "message": payload.get("message", payload.get("text", "")).strip(),
        "user_id": payload.get("user_id", payload.get("sender_id", "")),
        "user_name": payload.get("user_name", payload.get("sender_name", "")).strip(),
        "user_phone": payload.get("user_phone", payload.get("phone", "")).strip(),
        "user_email": payload.get("user_email", payload.get("email", "")).strip(),
        "timestamp": datetime.fromisoformat(payload.get("timestamp", datetime.now().isoformat())),
        "raw_payload": payload
    }
