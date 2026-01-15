from fastapi import FastAPI
from api.webhooks import router as webhook_router

app = FastAPI(title="Lead Capture Agent")
app.include_router(webhook_router)

@app.get("/")
def root():
    return {"status": "Agent running"}

# TEMP route to test AI/lead service
@app.get("/test-lead")
def test_lead():
    from app.services.lead_service import process_lead
    dummy = {
        "channel": "instagram",
        "user_id": "123",
        "message": "I want to buy a product urgently"
    }
    process_lead(dummy)
    return {"message": "Lead processed, check terminal for score"}