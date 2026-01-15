from app.core.normalizer import normalize
from app.ai.llm import analyze_message
from app.core.lead_scoring import score_lead

def process_lead(payload):
    data = normalize(payload)
    ai_data = analyze_message(data["text"])
    score = score_lead(ai_data)
    print("Lead Score:", score)
