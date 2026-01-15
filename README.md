# Lead Capture Agent - Complete Implementation

A smart, multi-channel lead capture system that listens to messages from WhatsApp, Instagram, and Website chat, understands intent using LLM, scores leads intelligently, and stores results in a database for export.

## 🧠 Architecture Overview

The system follows a 7-step pipeline:

1. **Receive** → Message arrives from any channel (WhatsApp/Instagram/Website)
2. **Normalize** → Convert to standard format (channel-agnostic)
3. **Analyze** → Extract intent, urgency, contact info using LLM
4. **Score** → Calculate lead value (0-100+)
5. **Store** → Save to database with full audit trail
6. **Filter** → Retrieve by quality (HOT/WARM/COLD)
7. **Export** → Output to Excel or other formats

## ✅ What's Implemented

### Step 1-3: Message Reception & Normalization ✓
- **Files**: [app/api/webhooks.py](app/api/webhooks.py), [app/core/normalizer.py](app/core/normalizer.py)
- Handles WhatsApp, Instagram, Website payloads
- Converts all formats to standard structure:
  ```python
  {
    "channel": "whatsapp|instagram|website",
    "message": "...",
    "user_id": "...",
    "user_name": "...",
    "user_email": "...",
    "user_phone": "...",
    "timestamp": datetime
  }
  ```

### Step 4: LLM-Based Analysis ✓
- **Files**: [app/gpt/llm.py](app/gpt/llm.py), [app/gpt/prompts.py](app/gpt/prompts.py)
- **Supported Providers**:
  - ✅ Mistral AI (API)
  - ✅ Google Gemini (API)
  - ✅ Ollama (Local)
- **Extracts**:
  - Intent: buy, question, complaint, inquiry
  - Urgency: low, medium, high
  - Contact info: name, email, phone
  - Budget (if mentioned)
  - Category: general, premium, enterprise, support
- **Fallback**: Keyword-based extraction if LLM fails

### Step 5: Intelligent Lead Scoring ✓
- **Files**: [app/core/lead_scoring.py](app/core/lead_scoring.py)
- **Scoring Factors**:
  - Intent (0-50 points)
  - Urgency (0-30 points)
  - Category bonus (0-30 points)
  - Contact info completeness (0-40 points)
  - Data source bonus (0-10 points)
- **Quality Labels**:
  - **HOT** (≥60): Immediate sales opportunity
  - **WARM** (40-59): Needs follow-up
  - **COLD** (<40): Low priority

### Step 6: Database Storage ✓
- **Files**: [app/db/models.py](app/db/models.py), [app/db/database.py](app/db/database.py)
- **Tables**:
  - `leads`: Main lead records
  - `lead_analyses`: Detailed AI analysis
  - `messages`: Raw message audit trail
- **Database Options**:
  - SQLite (default, zero setup)
  - PostgreSQL (for production)

### Step 7: Lead Service & Export ✓
- **Files**: [app/services/lead_service.py](app/services/lead_service.py), [app/core/exporter.py](app/core/exporter.py)
- **Orchestration**: Full pipeline in one function
- **Export Formats**: Excel with multi-sheet summaries
- **Filtering**: By quality, channel, date range

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8+
python --version

# Virtual environment (optional but recommended)
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
```

### Installation
```bash
# Install dependencies
pip install -r app/requirements.txt

# Create .env file
cp .env.example .env
```

### Configuration
Edit `.env`:
```bash
# Choose your LLM provider
LLM_PROVIDER=mistral              # or gemini, ollama
LLM_API_KEY=your_api_key          # Get from mistral.ai or console.cloud.google.com
LLM_MODEL=mistral-small-latest    # Model name

# Database (SQLite by default)
DATABASE_URL=sqlite:///./leads.db

# For PostgreSQL: postgresql://user:password@localhost/lead_agent
```

### Run Tests
```bash
# Validate the entire pipeline
python run_tests.py
```

Expected output: All tests should pass, showing:
- ✓ Multi-channel normalization
- ✓ LLM analysis (with fallback to keywords)
- ✓ Lead scoring
- ✓ Database storage
- ✓ Retrieval and filtering

### Start the API
```bash
# Development server
uvicorn app.main:app --reload --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 📡 API Endpoints

### POST `/api/webhook` - Receive Message
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

**Response**:
```json
{
  "status": "success",
  "data": {
    "lead_id": 1,
    "channel": "whatsapp",
    "analysis": {
      "intent": "buy",
      "urgency": "high",
      "name": "John"
    },
    "scoring": {
      "total_score": 80,
      "quality": "HOT"
    }
  }
}
```

### GET `/api/webhook/stats` - Statistics
```bash
curl http://localhost:8000/api/webhook/stats
```

### GET `/api/webhook/leads` - Get Leads
```bash
# All leads
curl http://localhost:8000/api/webhook/leads

# Only HOT leads
curl http://localhost:8000/api/webhook/leads?quality=HOT

# Limited results
curl http://localhost:8000/api/webhook/leads?limit=10
```

## 📊 Channel-Specific Payloads

### WhatsApp
```json
{
  "channel": "whatsapp",
  "from": "+1234567890",
  "contact_name": "John Doe",
  "message_text": "I want to buy...",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Instagram
```json
{
  "channel": "instagram",
  "sender_id": "insta_123",
  "sender_name": "Sarah",
  "sender_email": "sarah@example.com",
  "text": "Do you have...",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Website Chat
```json
{
  "channel": "website",
  "visitor_id": "session_456",
  "name": "Mike",
  "email": "mike@company.com",
  "phone": "555-0123",
  "chat": "We need help...",
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🔧 Configuration Guide

### LLM Providers

#### Mistral AI (Recommended)
1. Sign up: https://console.mistral.ai/
2. Get API key
3. Set in `.env`:
```bash
LLM_PROVIDER=mistral
LLM_MODEL=mistral-small-latest
LLM_API_KEY=xxxx
```

#### Google Gemini
1. Create project: https://console.cloud.google.com/
2. Enable Generative AI API
3. Get API key: https://makersuite.google.com/app/apikey
4. Set in `.env`:
```bash
LLM_PROVIDER=gemini
LLM_MODEL=gemini-pro
LLM_API_KEY=xxxx
```

#### Ollama (Local, Free)
1. Install: https://ollama.ai
2. Run: `ollama pull mistral`
3. Start: `ollama serve`
4. Set in `.env`:
```bash
LLM_PROVIDER=ollama
LLM_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
```

### Database

#### SQLite (Default)
Works out of the box, no setup needed. Good for development/small scale.

#### PostgreSQL (Production)
```bash
# Install driver
pip install psycopg2-binary

# Set in .env
DATABASE_URL=postgresql://user:password@localhost:5432/lead_agent
```

## 📂 Project Structure

```
app/
├── main.py                 # FastAPI app, startup/shutdown
├── config.py              # Configuration & environment
├── API.md                 # API documentation
├── api/
│   └── webhooks.py        # HTTP endpoints
├── core/
│   ├── normalizer.py      # Channel-agnostic formatting
│   ├── lead_scoring.py    # Lead valuation logic
│   └── exporter.py        # Excel export
├── gpt/
│   ├── llm.py             # LLM API integration
│   └── prompts.py         # Prompt templates
├── db/
│   ├── database.py        # SQLAlchemy setup
│   └── models.py          # Data models
├── services/
│   ├── lead_service.py    # Pipeline orchestration
│   └── notification_service.py
└── tests/
    └── test_lead_flow.py  # End-to-end tests
```

## 🧪 Testing

Run the complete test suite:
```bash
python run_tests.py
```

This tests:
1. WhatsApp message normalization
2. Instagram DM processing
3. Website chat handling
4. LLM analysis (with API key or fallback)
5. Lead scoring logic
6. Database storage
7. Data retrieval and filtering

## 📊 Scoring Example

**Input Message**: "Hi, I want to buy your premium package urgently. My email is john@example.com"

**AI Analysis**:
- Intent: `buy` → +50 points
- Urgency: `high` → +30 points
- Category: `general` → 0 points
- Contact info: email provided → +10 points

**Final Score**: 90 → **HOT Lead** 🔥

## 🔐 Environment Variables

```bash
# LLM
LLM_PROVIDER=mistral|gemini|ollama
LLM_MODEL=mistral-small-latest
LLM_API_KEY=your_key
OLLAMA_BASE_URL=http://localhost:11434

# Database
DATABASE_URL=sqlite:///./leads.db
SQLALCHEMY_ECHO=False

# Export
EXPORT_PATH=./exports

# Logging
DEBUG=False
```

## 🎯 Next Steps (Enterprise)

Once you have the foundation working:

1. **Add Authentication**: JWT tokens, API keys
2. **Webhooks Scaling**: Use message queues (Redis, RabbitMQ)
3. **Dashboard**: React/Vue frontend for lead management
4. **Notifications**: Send alerts to sales team
5. **Analytics**: Track conversion rates, response times
6. **Multi-tenancy**: Support multiple clients
7. **CRM Integration**: Sync with Salesforce, HubSpot
8. **Auto-response**: Send templated replies on WhatsApp

## 🐛 Troubleshooting

### "LLM Analysis Error: 401 Client Error"
- Your LLM API key is missing or invalid
- Get key from mistral.ai or google console
- System will fallback to keyword-based analysis

### "Database locked"
- Close any other instances accessing leads.db
- Or switch to PostgreSQL for multi-process handling

### "Module not found"
```bash
# Reinstall dependencies
pip install -r app/requirements.txt
```

### Unicode encoding errors
- Only happens on Windows CMD, not PowerShell
- Use PowerShell or fix Windows terminal encoding

## 📄 License

This is a demonstration project. Feel free to use and modify.

---

**Built with**: FastAPI, SQLAlchemy, Pandas, Mistral/Gemini/Ollama LLM

**Last Updated**: January 15, 2026
