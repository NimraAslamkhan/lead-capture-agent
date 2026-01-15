# API Documentation - Lead Capture Agent

## Overview

The Lead Capture Agent provides a unified webhook interface for receiving messages from multiple channels and intelligently processing them into qualified leads.

## Base URL

```
http://localhost:8000/api
```

---

## Endpoints

### 1. POST `/webhook` - Receive Message

Receive and process a message from any channel.

**Request Body:**

```json
{
  "channel": "whatsapp|instagram|website",
  "user_id": "unique_identifier",
  "message": "message_text",
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "user_phone": "+1234567890",
  "timestamp": "2024-01-15T10:30:00"
}
```

**Example - WhatsApp:**
```bash
curl -X POST http://localhost:8000/api/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "whatsapp",
    "from": "+1234567890",
    "contact_name": "John",
    "message_text": "I want to buy your product urgently",
    "timestamp": "2024-01-15T10:30:00"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Lead received and processed",
  "data": {
    "lead_id": 1,
    "channel": "whatsapp",
    "user_id": "+1234567890",
    "analysis": {
      "intent": "buy",
      "urgency": "high",
      "category": "general",
      "name": "John",
      "email": "",
      "phone": "+1234567890",
      "budget": ""
    },
    "scoring": {
      "total_score": 85,
      "quality": "HOT",
      "breakdown": {
        "intent": 50,
        "urgency": 30,
        "category": 0,
        "contact_info": 10,
        "data_source_bonus": 5
      },
      "contact_completeness": 1
    }
  }
}
```

---

### 2. GET `/webhook/stats` - Get Statistics

Retrieve overall lead statistics.

**Response:**
```json
{
  "status": "success",
  "stats": {
    "total_leads": 15,
    "hot_leads": 5,
    "warm_leads": 6,
    "cold_leads": 4
  }
}
```

---

### 3. GET `/webhook/leads` - Get Leads

Retrieve leads with optional filtering.

**Query Parameters:**
- `quality`: Filter by HOT, WARM, or COLD (optional)
- `limit`: Maximum results, default 50 (optional)

**Examples:**
```bash
# Get all leads
curl http://localhost:8000/api/webhook/leads

# Get only HOT leads
curl http://localhost:8000/api/webhook/leads?quality=HOT

# Get top 10 leads
curl http://localhost:8000/api/webhook/leads?limit=10

# Get top 5 WARM leads
curl http://localhost:8000/api/webhook/leads?quality=WARM&limit=5
```

**Response:**
```json
{
  "status": "success",
  "count": 3,
  "leads": [
    {
      "id": 1,
      "channel": "whatsapp",
      "user_name": "John Doe",
      "user_email": "john@example.com",
      "user_phone": "+1234567890",
      "message": "I want to buy your product urgently...",
      "intent": "buy",
      "urgency": "high",
      "score": 85,
      "quality": "HOT",
      "created_at": "2024-01-15T10:30:00",
      "contact_completeness": 2
    }
  ]
}
```

---

## Channel-Specific Formats

### WhatsApp Webhook
```json
{
  "channel": "whatsapp",
  "from": "phone_number",
  "contact_name": "name",
  "message_text": "content",
  "timestamp": "iso_datetime"
}
```

### Instagram Webhook
```json
{
  "channel": "instagram",
  "sender_id": "user_id",
  "sender_name": "name",
  "sender_email": "email",
  "text": "content",
  "timestamp": "iso_datetime"
}
```

### Website Chat Webhook
```json
{
  "channel": "website",
  "visitor_id": "session_id",
  "name": "visitor_name",
  "email": "visitor_email",
  "phone": "phone_number",
  "chat": "message_content",
  "timestamp": "iso_datetime"
}
```

---

## Lead Scoring

The agent assigns a score to each lead (0-100+) based on:

| Factor | Points |
|--------|--------|
| Intent: Buy | 50 |
| Intent: Question | 20 |
| Intent: Inquiry | 10 |
| Intent: Complaint | 0 |
| Urgency: High | 30 |
| Urgency: Medium | 15 |
| Urgency: Low | 0 |
| Category: Enterprise | 30 |
| Category: Premium | 25 |
| Category: General | 0 |
| Category: Support | -10 |
| Name Provided | 10 |
| Email Provided | 10 |
| Phone Provided | 10 |
| Contact Completeness (2+ fields) | 10 |
| Data Source Bonus | 5 |

### Quality Labels

- **HOT** 🔥: Score ≥ 60 (Immediate sales opportunity)
- **WARM** 🔆: Score 40-59 (Follow-up needed)
- **COLD** ❄️: Score < 40 (Low priority)

---

## Setup & Configuration

### 1. Environment Variables

Create a `.env` file:

```bash
# LLM Provider
LLM_PROVIDER=mistral  # or gemini, ollama
LLM_MODEL=mistral-small-latest
LLM_API_KEY=your_api_key_here

# Database
DATABASE_URL=sqlite:///./leads.db

# Exports
EXPORT_PATH=./exports
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Server

```bash
uvicorn app.main:app --reload
```

---

## Supported LLM Providers

### Mistral AI (Recommended)
```env
LLM_PROVIDER=mistral
LLM_MODEL=mistral-small-latest
LLM_API_KEY=your_mistral_key
```
Get API key: https://console.mistral.ai/

### Google Gemini
```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-pro
LLM_API_KEY=your_gemini_key
```
Get API key: https://makersuite.google.com/app/apikey

### Local Ollama
```env
LLM_PROVIDER=ollama
LLM_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Testing

Run the end-to-end test:

```bash
python run_tests.py
```

This validates:
1. ✅ Message normalization from all channels
2. ✅ LLM-based analysis
3. ✅ Lead scoring logic
4. ✅ Database storage
5. ✅ Lead filtering and retrieval
6. ✅ Export capabilities
