# Quick Reference - Lead Capture Agent

## 🚀 Start Here (5 minutes)

```bash
# 1. Install
pip install -r app/requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env: Add your LLM_API_KEY

# 3. Test
python run_tests.py

# 4. Run
uvicorn app.main:app --reload
# Visit: http://localhost:8000/docs
```

## 📊 The 7-Step Pipeline

```
1. RECEIVE    → Message from WhatsApp/Instagram/Website
2. NORMALIZE  → Convert to standard format
3. ANALYZE    → Extract intent, urgency, contact info (LLM)
4. SCORE      → Calculate lead value (0-100+)
5. STORE      → Save to database
6. FILTER     → Retrieve by quality (HOT/WARM/COLD)
7. EXPORT     → Output to Excel
```

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/webhook` | Send message from any channel |
| GET | `/api/webhook/stats` | Get overall statistics |
| GET | `/api/webhook/leads` | Get leads (with filtering) |
| GET | `/health` | Health check |
| GET | `/` | Root/documentation |

## 📨 Send a Message

```bash
curl -X POST http://localhost:8000/api/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "whatsapp",
    "from": "+1234567890",
    "contact_name": "John",
    "message_text": "I want to buy urgently",
    "timestamp": "2024-01-15T10:30:00"
  }'
```

## 🎯 Scoring Rules

| Factor | Points | Example |
|--------|--------|---------|
| Intent: Buy | 50 | "I want to purchase" |
| Intent: Question | 20 | "Do you have..." |
| Intent: Inquiry | 10 | Generic question |
| Intent: Complaint | 0 | Issue reported |
| Urgency: High | 30 | "urgent", "ASAP" |
| Urgency: Medium | 15 | "soon", "quickly" |
| Urgency: Low | 0 | Default |
| Contact: Name | 10 | User provided name |
| Contact: Email | 10 | Valid email present |
| Contact: Phone | 10 | Valid phone present |
| Category: Enterprise | 30 | "enterprise solution" |
| Category: Premium | 25 | "premium package" |

## 🏷️ Lead Quality

| Quality | Score | Action |
|---------|-------|--------|
| HOT | ≥60 | Call immediately |
| WARM | 40-59 | Follow-up needed |
| COLD | <40 | Archive |

## 🔧 Configuration

### LLM Provider (Choose One)

**Option 1: Mistral AI (Recommended)**
```bash
LLM_PROVIDER=mistral
LLM_MODEL=mistral-small-latest
LLM_API_KEY=xxxx_from_mistral.ai
```

**Option 2: Google Gemini**
```bash
LLM_PROVIDER=gemini
LLM_API_KEY=xxxx_from_google
```

**Option 3: Ollama (Free Local)**
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
# First: ollama pull mistral
#        ollama serve
```

### Database

**SQLite** (Default)
```bash
DATABASE_URL=sqlite:///./leads.db
```

**PostgreSQL** (Production)
```bash
DATABASE_URL=postgresql://user:pass@localhost/lead_agent
```

## 📂 Key Files

```
app/
├── main.py                 # FastAPI app setup
├── config.py              # Environment config
├── api/webhooks.py        # HTTP endpoints
├── core/normalizer.py     # Channel normalization
├── core/lead_scoring.py   # Lead valuation
├── core/exporter.py       # Excel export
├── gpt/llm.py             # LLM integration
├── db/models.py           # Database schema
├── db/database.py         # DB initialization
├── services/lead_service.py  # Pipeline orchestration
└── tests/test_lead_flow.py   # End-to-end tests
```

## 🧪 Testing

```bash
# Run all tests
python run_tests.py

# Expected output:
# Tests Run: 4
# PASS: 4 (WhatsApp, Instagram, Website, Generic)
# FAIL: 0
# Result: ALL TESTS PASSED!
```

## 📊 Database Tables

### leads
- id, channel, user_id, user_name, user_email, user_phone
- message, intent, urgency, category
- total_score, quality, contact_completeness
- created_at, updated_at, processed, exported

### lead_analyses
- id, lead_id, intent, urgency, category, name, email, phone, budget
- created_at

### messages
- id, lead_id, channel, user_id, message_text
- raw_payload, received_at, processed_at

## 🔌 Channel Payloads

### WhatsApp
```json
{
  "channel": "whatsapp",
  "from": "+1234567890",
  "contact_name": "John",
  "message_text": "...",
  "timestamp": "ISO_DATETIME"
}
```

### Instagram
```json
{
  "channel": "instagram",
  "sender_id": "123",
  "sender_name": "Sarah",
  "sender_email": "sarah@example.com",
  "text": "...",
  "timestamp": "ISO_DATETIME"
}
```

### Website
```json
{
  "channel": "website",
  "visitor_id": "456",
  "name": "Mike",
  "email": "mike@company.com",
  "phone": "555-0123",
  "chat": "...",
  "timestamp": "ISO_DATETIME"
}
```

## 🐳 Docker Quick Start

```bash
# Build
docker build -f app/docker/Dockerfile -t lead-agent .

# Run
docker run -p 8000:8000 \
  -e LLM_PROVIDER=mistral \
  -e LLM_API_KEY=your_key \
  lead-agent
```

## ⚡ Common Tasks

### Get all HOT leads
```bash
curl "http://localhost:8000/api/webhook/leads?quality=HOT"
```

### Get stats
```bash
curl http://localhost:8000/api/webhook/stats
```

### Export leads to Excel
```python
from app.services.lead_service import get_db
from app.core.exporter import export_all_leads

db = next(get_db())
export_all_leads(db)
# Creates: exports/leads_20240115_103000.xlsx
```

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| `401 Unauthorized` on LLM | Add LLM_API_KEY to .env |
| `ModuleNotFound` | `pip install -r app/requirements.txt` |
| Database locked | Close other instances, or use PostgreSQL |
| Slow responses | Switch to `mistral-small` model |
| Unicode errors | Use PowerShell on Windows (not CMD) |

## 📚 Resources

- [API Documentation](app/API.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Full README](README.md)
- [Mistral Docs](https://docs.mistral.ai)
- [Gemini Docs](https://ai.google.dev)
- [Ollama Docs](https://ollama.ai)

---

**Status**: ✅ Production Ready | **Last Updated**: Jan 15, 2026
