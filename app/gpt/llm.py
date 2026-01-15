import requests
import json
from app.config import LLM_PROVIDER, LLM_API_KEY, LLM_MODEL, OLLAMA_BASE_URL
from app.gpt.prompts import get_analysis_prompt

def analyze_message(text, channel="unknown"):
    """
    Analyze message using LLM to extract:
    - Intent (buy, question, complaint, inquiry)
    - Urgency (low, medium, high)
    - Contact info (name, email, phone)
    - Budget (if mentioned)
    """
    
    if not text or not isinstance(text, str):
        return get_default_analysis()
    
    try:
        if LLM_PROVIDER == "mistral":
            return _analyze_with_mistral(text, channel)
        elif LLM_PROVIDER == "gemini":
            return _analyze_with_gemini(text, channel)
        elif LLM_PROVIDER == "ollama":
            return _analyze_with_ollama(text, channel)
        else:
            return get_default_analysis()
    except Exception as e:
        print(f"LLM Analysis Error: {e}")
        return get_default_analysis()


def _analyze_with_mistral(text, channel):
    """Call Mistral API for analysis"""
    url = "https://api.mistral.ai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLM_API_KEY}"
    }
    
    prompt = get_analysis_prompt(text, channel)
    
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    
    return _parse_llm_response(content)


def _analyze_with_gemini(text, channel):
    """Call Google Gemini API for analysis"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={LLM_API_KEY}"
    
    prompt = get_analysis_prompt(text, channel)
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    result = response.json()
    content = result["candidates"][0]["content"]["parts"][0]["text"]
    
    return _parse_llm_response(content)


def _analyze_with_ollama(text, channel):
    """Call local Ollama instance for analysis"""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    
    prompt = get_analysis_prompt(text, channel)
    
    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.3
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    result = response.json()
    content = result["response"]
    
    return _parse_llm_response(content)


def _parse_llm_response(content):
    """Parse LLM response and extract structured data"""
    try:
        # Try to extract JSON from response
        if "{" in content and "}" in content:
            json_str = content[content.find("{"):content.rfind("}")+1]
            data = json.loads(json_str)
            
            # Normalize keys
            return {
                "intent": data.get("intent", "inquiry").lower(),
                "urgency": data.get("urgency", "low").lower(),
                "name": data.get("name", ""),
                "email": data.get("email", ""),
                "phone": data.get("phone", ""),
                "budget": data.get("budget", ""),
                "category": data.get("category", "general")
            }
    except:
        pass
    
    # Fallback to keyword-based extraction
    return _extract_by_keywords(content)


def _extract_by_keywords(text):
    """Fallback: Extract info using keyword matching"""
    text_lower = text.lower()
    
    # Intent extraction
    intent = "inquiry"
    if any(word in text_lower for word in ["buy", "purchase", "want to buy", "need", "order"]):
        intent = "buy"
    elif any(word in text_lower for word in ["question", "how", "what", "when", "why", "where"]):
        intent = "question"
    elif any(word in text_lower for word in ["complaint", "problem", "issue", "not working", "broken"]):
        intent = "complaint"
    
    # Urgency extraction
    urgency = "low"
    if any(word in text_lower for word in ["urgent", "asap", "immediately", "now", "today", "emergency"]):
        urgency = "high"
    elif any(word in text_lower for word in ["soon", "quickly", "fast", "quick"]):
        urgency = "medium"
    
    return {
        "intent": intent,
        "urgency": urgency,
        "name": "",
        "email": "",
        "phone": "",
        "budget": "",
        "category": "general"
    }


def get_default_analysis():
    """Return default analysis when LLM fails"""
    return {
        "intent": "inquiry",
        "urgency": "low",
        "name": "",
        "email": "",
        "phone": "",
        "budget": "",
        "category": "general"
    }