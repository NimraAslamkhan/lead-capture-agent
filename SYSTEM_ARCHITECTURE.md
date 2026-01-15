# 🏗️ SYSTEM ARCHITECTURE & DATA FLOW

## Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CUSTOMER CHANNELS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│    💬 WhatsApp    │    📷 Instagram   │    🌐 Website    │    📧 Email       │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                              ↓ (customer message)
┌─────────────────────────────────────────────────────────────────────────────┐
│                       YOUR AGENT (Backend)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  STEP 1: RECEIVE             STEP 2: NORMALIZE          STEP 3: ANALYZE     │
│  ┌────────────────┐          ┌──────────────┐           ┌────────────────┐  │
│  │ API Webhook    │──→       │ Channel      │──→        │ LLM (AI)       │  │
│  │ receives msg   │          │ Normalizer   │           │ Intent detect  │  │
│  │ from customer  │          │ converts to  │           │ sentiment      │  │
│  │                │          │ standard     │           │ analysis       │  │
│  │ Method: POST   │          │ format       │           │                │  │
│  │ /api/webhook   │          └──────────────┘           └────────────────┘  │
│  └────────────────┘                                                          │
│                                                                               │
│  STEP 4: SCORE               STEP 5: STORE             STEP 6: ANALYZE     │
│  ┌────────────────┐          ┌──────────────┐           ┌────────────────┐  │
│  │ Scoring Engine │──→       │ Database     │──→        │ Extract        │  │
│  │ 7-factor model │          │ SQLite/PG    │           │ structured data│  │
│  │ calculates:    │          │ saves to:    │           │ store details  │  │
│  │ - Intent       │          │ - Leads      │           │                │  │
│  │ - Urgency      │          │ - Analyses   │           └────────────────┘  │
│  │ - Contact Info │          │ - Messages   │                                │
│  │ - Channel      │          └──────────────┘           STEP 7: EXPORT     │
│  │ Score 0-100    │                                     ┌────────────────┐  │
│  │ Quality rating │                                     │ Export Engine  │  │
│  └────────────────┘                                     │ Excel/CSV      │  │
│                                                          │ download ready │  │
│                                                          └────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓ (processed data)
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  🌐 WEB DASHBOARD              📊 TABLE DISPLAY           📥 DOWNLOADS       │
│  ┌──────────────────┐          ┌─────────────────┐       ┌────────────────┐ │
│  │ Beautiful        │          │ Lead #  │ Name  │       │ Excel File     │ │
│  │ HTML interface   │──→       │ 1      │ Ahmed │──→    │ .csv format    │ │
│  │ Real-time data   │          │ 2      │ Sarah │       │ Ready to       │ │
│  │ Auto-refresh 30s │          │ 3      │ Hassan│       │ download       │ │
│  │ Statistics cards │          │ Score  │ Grade │       └────────────────┘ │
│  │ Filter & search  │          └─────────────────┘                          │
│  │ Mobile friendly  │                                   📧 SHARING          │
│  │ Download buttons │                                   ┌────────────────┐ │
│  └──────────────────┘                                   │ Send link to   │ │
│                                                          │ team/clients   │ │
│                                                          │ Share view     │ │
│                                                          │ Grant access   │ │
│                                                          └────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Data Flow

```
MESSAGE RECEIVED
    │
    ├─→ ┌──────────────┐
    │   │ NORMALIZE    │  Extract: name, phone, email, message, channel
    │   └──────────────┘
    │   Result: Standard format
    │
    ├─→ ┌──────────────┐
    │   │ LLM ANALYZE  │  Extract: intent, urgency, category
    │   │ (AI)         │  • Mistral API
    │   │              │  • Gemini API  
    │   │              │  • Ollama local
    │   │              │  • Keyword fallback
    │   └──────────────┘
    │   Result: intent + analysis
    │
    ├─→ ┌──────────────┐
    │   │ SCORE        │  Calculate score (0-100)
    │   │ (7 factors)  │  • Intent points
    │   │              │  • Urgency points
    │   │              │  • Contact quality
    │   │              │  • Channel score
    │   │              │  • Data quality
    │   │              │  • Message length
    │   │              │  • Bonus points
    │   └──────────────┘
    │   Result: 0-100 score
    │
    ├─→ ┌──────────────┐
    │   │ GRADE        │  Quality = HOT | WARM | COLD
    │   │ QUALITY      │  • HOT:  ≥60  (act now!)
    │   │              │  • WARM: 40-59 (follow up)
    │   │              │  • COLD: <40   (later)
    │   └──────────────┘
    │   Result: Quality label
    │
    ├─→ ┌──────────────┐
    │   │ STORE IN DB  │  Save to database:
    │   │              │  • Table: Leads (main record)
    │   │              │  • Table: LeadAnalysis (details)
    │   │              │  • Table: Message (audit log)
    │   └──────────────┘
    │   Result: Stored, ID assigned
    │
    ├─→ ┌──────────────┐
    │   │ READY FOR    │  Dashboard shows:
    │   │ DASHBOARD    │  • In statistics
    │   │              │  • In lead table
    │   │              │  • With color coding
    │   │              │  • Instantly visible
    │   └──────────────┘
    │
    └─→ 🎉 COMPLETE
```

---

## Database Schema

```
LEADS TABLE
┌─────────────────────────────────────────────────────┐
│ id           │ Primary key                           │
│ user_name    │ Customer name                         │
│ user_email   │ Customer email                        │
│ user_phone   │ Customer phone                        │
│ channel      │ Source (whatsapp/instagram/website)   │
│ message      │ Original message from customer        │
│ intent       │ AI-detected intent (Buy/Question...)  │
│ urgency      │ Urgency level (High/Medium/Low)       │
│ score        │ Final score (0-100)                   │
│ quality      │ Grade (HOT/WARM/COLD)                │
│ created_at   │ Timestamp when received               │
│ exported     │ Has this been exported? (Y/N)         │
└─────────────────────────────────────────────────────┘

LEAD_ANALYSIS TABLE
┌─────────────────────────────────────────────────────┐
│ id           │ Primary key                           │
│ lead_id      │ Reference to Leads table              │
│ category     │ Detected category                     │
│ sentiment    │ Sentiment analysis (positive/neg)     │
│ confidence   │ AI confidence (0-100)                 │
│ extracted_data│ Structured extracted data             │
│ created_at   │ Analysis timestamp                    │
└─────────────────────────────────────────────────────┘

MESSAGE TABLE
┌─────────────────────────────────────────────────────┐
│ id           │ Primary key                           │
│ lead_id      │ Reference to Leads table              │
│ original_msg │ Raw message from customer             │
│ processed_msg│ Cleaned/normalized version            │
│ metadata     │ Additional info (IP, device, etc)     │
│ created_at   │ Message received timestamp            │
└─────────────────────────────────────────────────────┘
```

---

## API Endpoints

```
WEBHOOK ENDPOINT
┌──────────────────────────────────────────────────────┐
│ POST /api/webhook                                    │
├──────────────────────────────────────────────────────┤
│ Receives message from customer                       │
│ Processes through pipeline                           │
│ Stores in database                                   │
│ Returns confirmation                                 │
│                                                      │
│ Input: {                                             │
│   "phone": "+923001234567",                          │
│   "message": "I want to buy...",                     │
│   "channel": "whatsapp",                             │
│   "sender_name": "Ahmed"                             │
│ }                                                    │
│                                                      │
│ Output: {                                            │
│   "status": "success",                               │
│   "lead_id": 1,                                      │
│   "quality": "HOT",                                  │
│   "score": 85                                        │
│ }                                                    │
└──────────────────────────────────────────────────────┘

LEADS ENDPOINT
┌──────────────────────────────────────────────────────┐
│ GET /api/webhook/leads?limit=100                    │
├──────────────────────────────────────────────────────┤
│ Returns all leads from database                      │
│ Supports pagination with limit                       │
│ Used by dashboard to display table                   │
│                                                      │
│ Output: {                                            │
│   "status": "success",                               │
│   "leads": [                                         │
│     {                                                │
│       "id": 1,                                       │
│       "user_name": "Ahmed",                          │
│       "user_email": "ahmed@...",                     │
│       "score": 85,                                   │
│       "quality": "HOT",                              │
│       "created_at": "2024-01-15T10:30:00"            │
│     },                                               │
│     ...                                              │
│   ]                                                  │
│ }                                                    │
└──────────────────────────────────────────────────────┘

STATS ENDPOINT
┌──────────────────────────────────────────────────────┐
│ GET /api/webhook/stats                              │
├──────────────────────────────────────────────────────┤
│ Returns statistics summary                           │
│ Used by dashboard statistics cards                   │
│                                                      │
│ Output: {                                            │
│   "status": "success",                               │
│   "total_leads": 4,                                  │
│   "hot_leads": 2,                                    │
│   "warm_leads": 1,                                   │
│   "cold_leads": 1                                    │
│ }                                                    │
└──────────────────────────────────────────────────────┘
```

---

## Component Breakdown

```
FRONTEND (Dashboard)
┌─────────────────────────────────────────────────────┐
│ dashboard.html (600+ lines)                         │
│ ├─ HTML Structure                                   │
│ │  ├─ Header                                        │
│ │  ├─ Statistics Cards                              │
│ │  ├─ Controls (filter, buttons)                    │
│ │  └─ Table with all leads                          │
│ ├─ CSS Styling (600+ lines)                         │
│ │  ├─ Gradient design                               │
│ │  ├─ Responsive layout                             │
│ │  ├─ Color coding system                           │
│ │  ├─ Animations & transitions                      │
│ │  └─ Mobile optimizations                          │
│ └─ JavaScript (200+ lines)                          │
│    ├─ Fetch leads from API                          │
│    ├─ Render table dynamically                      │
│    ├─ Filter functionality                          │
│    ├─ Download to Excel/CSV                         │
│    ├─ Auto-refresh every 30 seconds                 │
│    └─ Error handling                                │
└─────────────────────────────────────────────────────┘

BACKEND (FastAPI)
┌─────────────────────────────────────────────────────┐
│ app/main.py - FastAPI Application                  │
│ ├─ Startup/shutdown events                          │
│ ├─ CORS configuration                               │
│ ├─ Static file mounting (dashboard)                 │
│ └─ Route registration                               │
│                                                      │
│ app/api/webhooks.py - API Endpoints                │
│ ├─ POST /api/webhook (receive messages)             │
│ ├─ GET /api/webhook/leads (get all leads)           │
│ └─ GET /api/webhook/stats (get statistics)          │
│                                                      │
│ app/services/lead_service.py - Pipeline            │
│ ├─ process_lead() - Main orchestration              │
│ │  ├─ normalize()                                   │
│ │  ├─ analyze()                                     │
│ │  ├─ score()                                       │
│ │  └─ store()                                       │
│ ├─ get_leads() - Query database                     │
│ └─ get_stats() - Calculate statistics               │
└─────────────────────────────────────────────────────┘

CORE LOGIC
┌─────────────────────────────────────────────────────┐
│ app/core/normalizer.py                             │
│ ├─ _normalize_whatsapp()                            │
│ ├─ _normalize_instagram()                           │
│ ├─ _normalize_website()                             │
│ └─ _normalize_generic()                             │
│                                                      │
│ app/gpt/llm.py - LLM Integration                   │
│ ├─ analyze_message() - Main entry point             │
│ ├─ _analyze_with_mistral()                          │
│ ├─ _analyze_with_gemini()                           │
│ ├─ _analyze_with_ollama()                           │
│ └─ Fallback to keywords                             │
│                                                      │
│ app/core/lead_scoring.py                           │
│ ├─ score_lead() - 7-factor algorithm                │
│ ├─ determine_quality() - HOT/WARM/COLD              │
│ ├─ is_valid_email()                                 │
│ └─ is_valid_phone()                                 │
└─────────────────────────────────────────────────────┘

DATABASE
┌─────────────────────────────────────────────────────┐
│ app/db/models.py - SQLAlchemy Models               │
│ ├─ Lead Model                                       │
│ ├─ LeadAnalysis Model                               │
│ └─ Message Model                                    │
│                                                      │
│ app/db/database.py - Database Setup                │
│ ├─ init_db() - Create tables                        │
│ ├─ get_db() - Session management                    │
│ └─ close_db() - Cleanup                             │
│                                                      │
│ SQLite Database (leads.db)                          │
│ ├─ leads table                                      │
│ ├─ lead_analysis table                              │
│ └─ message table                                    │
└─────────────────────────────────────────────────────┘
```

---

## Technology Stack

```
FRONTEND
├─ HTML5          - Structure
├─ CSS3           - Styling & animations
└─ JavaScript     - Interactivity & API calls

BACKEND
├─ FastAPI 0.40.0 - Web framework
├─ Python 3.10    - Programming language
├─ SQLAlchemy     - ORM
├─ Pydantic       - Data validation
└─ Requests       - HTTP client

DATABASE
├─ SQLite 3       - Local development
└─ PostgreSQL     - Production ready

LLM/AI
├─ Mistral AI API    - Cloud LLM
├─ Google Gemini API - Cloud LLM
├─ Ollama            - Local LLM
└─ Keyword fallback  - No API needed

DEPLOYMENT
├─ Docker          - Containerization
├─ AWS             - Cloud platform
├─ Heroku          - PaaS platform
└─ Render          - Modern hosting

UTILITIES
├─ Pandas          - Data manipulation
├─ OpenPyXL        - Excel export
└─ Python-dotenv   - Configuration
```

---

## Execution Flow Diagram

```
START: Customer sends message via WhatsApp
    │
    ├─→ Message reaches WhatsApp → Forwarded to your webhook
    │
    ├─→ RECEIVE: API receives message
    │   │ POST /api/webhook
    │   │ Body: {"phone": "+...", "message": "...", "channel": "whatsapp"}
    │   │
    │   └─→ Lead Created (ID: 1)
    │
    ├─→ NORMALIZE: Convert to standard format
    │   │ Input: Raw WhatsApp message
    │   │ Process: Extract name, phone, email, channel
    │   │ Output: Standardized lead data
    │   │
    │   └─→ Result: Clean data
    │
    ├─→ ANALYZE: LLM analyzes intent
    │   │ Try Mistral API
    │   │ If fails → Try Gemini API
    │   │ If fails → Try Ollama
    │   │ If fails → Use keywords
    │   │ Extract: intent, category, sentiment
    │   │
    │   └─→ Result: Intent = "Buy", Urgency = "High"
    │
    ├─→ SCORE: Calculate lead quality score
    │   │ Intent (Buy) = 50 points
    │   │ Urgency (High) = 30 points
    │   │ Phone valid = 20 points
    │   │ Message length = 10 points
    │   │ Channel (WhatsApp) = 10 points
    │   │ Bonus (complete contact) = 5 points
    │   │ Total = 85/100
    │   │
    │   └─→ Result: Score = 85
    │
    ├─→ GRADE: Determine quality
    │   │ If score ≥ 60 → HOT 🔥
    │   │ Else if ≥ 40 → WARM 🔆
    │   │ Else → COLD ❄️
    │   │
    │   └─→ Result: Quality = HOT
    │
    ├─→ STORE: Save to database
    │   │ INSERT INTO leads (...)
    │   │ INSERT INTO lead_analysis (...)
    │   │ INSERT INTO message (...)
    │   │
    │   └─→ Result: Stored in SQLite
    │
    ├─→ DASHBOARD: Display instantly
    │   │ JavaScript fetches /api/webhook/leads
    │   │ Table updates with new lead
    │   │ Statistics recalculate
    │   │ Color coding applied (Red for HOT)
    │   │
    │   └─→ Result: You see Ahmed Khan's lead immediately!
    │
    ├─→ YOU TAKE ACTION
    │   │ See Ahmed Khan (Score: 85, Quality: HOT)
    │   │ Click his phone number
    │   │ Call him immediately
    │   │ Ahmed: "Yes, I want to buy!"
    │   │ You: "Great, let me take your order"
    │   │
    │   └─→ Result: SALE ✅
    │
    └─→ END: Lead converted to customer!
```

---

## Real-Time Update Flow

```
Dashboard loaded (http://localhost:8000/static/dashboard.html)
    │
    ├─→ JavaScript runs: fetchLeads()
    │   │ GET /api/webhook/leads
    │   │ Receives JSON with all leads
    │   │ displayLeads(leads) renders table
    │   │ updateStats(leads) shows numbers
    │   │ Auto-refresh timer set: 30 seconds
    │   │
    │   └─→ Dashboard shows all leads ✓
    │
    ├─→ User sees dashboard with all leads
    │   │ Statistics: 4 total, 2 hot, 1 warm, 1 cold
    │   │ Table shows all lead details
    │   │ Colors show priorities (red=hot, orange=warm)
    │   │
    │   └─→ User ready to act ✓
    │
    ├─→ NEW MESSAGE ARRIVES (Customer #5)
    │   │ Backend processes through pipeline
    │   │ Stored in database
    │   │ Ready to be fetched
    │   │
    │   └─→ Waiting for next refresh...
    │
    ├─→ EVERY 30 SECONDS: Auto-refresh
    │   │ JavaScript calls fetchLeads() again
    │   │ Gets latest data from database
    │   │ New customer #5 appears in table!
    │   │ Statistics update: 5 total, 2 hot
    │   │ Timestamp updates
    │   │
    │   └─→ User sees new lead instantly ✓
    │
    └─→ No manual refresh needed! Everything automatic!
```

---

## Scaling Architecture (Future)

```
Single Server (Current)
┌──────────────────────────────┐
│ All components on one box    │
│ √ Simple setup               │
│ √ Easy to test               │
│ √ Good for <1000 leads/day   │
└──────────────────────────────┘
          ↓ (scale up to)
Microservices (Future)
┌──────────────┬────────────┬──────────────┐
│ API Server   │ Workers    │ Database     │
│ (FastAPI)    │ (Queue)    │ (PostgreSQL) │
├──────────────┼────────────┼──────────────┤
│ Routes       │ Process    │ All data     │
│ Webhooks     │ Pipeline   │ Replicated   │
│ Dashboard    │ (Celery)   │ Backup       │
└──────────────┴────────────┴──────────────┘
          ↓ (scale to millions)
Cloud Distributed (Enterprise)
┌────────────────────────────────────────┐
│ CDN (Static files)                     │
├────────────────────────────────────────┤
│ Load Balancer                          │
├─────────┬─────────┬──────────┬─────────┤
│ API 1   │ API 2   │ API 3    │ API N   │
├─────────┴─────────┴──────────┴─────────┤
│ Message Queue (RabbitMQ)               │
├─────────┬─────────┬──────────┬─────────┤
│ Worker1 │ Worker2 │ Worker3  │ WorkerN │
├─────────────────────────────────────────┤
│ Database Cluster (PostgreSQL)           │
│ Cache Layer (Redis)                     │
│ Backups (S3)                            │
└─────────────────────────────────────────┘
```

---

## Summary

Your system has:
- **7-step pipeline** processing each lead
- **4-channel support** (WhatsApp, Instagram, Website, Email)
- **3 LLM providers** (Mistral, Gemini, Ollama)
- **Beautiful dashboard** (HTML/CSS/JavaScript)
- **Real-time updates** (every 30 seconds)
- **Download functionality** (Excel/CSV)
- **Professional database** (SQLite/PostgreSQL)
- **Production ready** (tested and documented)
- **Infinitely scalable** (architecture supports growth)

Everything works together to capture, analyze, score, and display leads in real-time! 🚀
