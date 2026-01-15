# Deployment & Production Setup Guide

## Local Development

### 1. Setup
```bash
# Navigate to project
cd d:\lead-capture-agent

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r app/requirements.txt

# Create .env
copy .env.example .env
```

### 2. Configure Environment
Edit `.env`:
```bash
# Option 1: Use Mistral AI (Recommended)
LLM_PROVIDER=mistral
LLM_MODEL=mistral-small-latest
LLM_API_KEY=paste_your_key_here

# Option 2: Use Google Gemini
# LLM_PROVIDER=gemini
# LLM_API_KEY=paste_your_key_here

# Option 3: Use Local Ollama (Free)
# LLM_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434
```

### 3. Run Tests
```bash
python run_tests.py
```

Expected: All 4 tests pass ✓

### 4. Start Server
```bash
# Development mode
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Visit: http://localhost:8000/docs

## Docker Deployment

### 1. Build Docker Image
```bash
# From project root
docker build -f app/docker/Dockerfile -t lead-capture-agent:latest .
```

### 2. Run Container
```bash
docker run -d \
  --name lead-agent \
  -p 8000:8000 \
  -e LLM_PROVIDER=mistral \
  -e LLM_API_KEY=your_key \
  -e DATABASE_URL=sqlite:///./data/leads.db \
  -v $(pwd)/exports:/app/exports \
  -v $(pwd)/data:/app/data \
  lead-capture-agent:latest
```

### 3. Docker Compose (Recommended)
Edit `app/docker/docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build:
      context: ../..
      dockerfile: app/docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      LLM_PROVIDER: mistral
      LLM_API_KEY: ${LLM_API_KEY}
      DATABASE_URL: postgresql://user:password@db:5432/lead_agent
      EXPORT_PATH: /app/exports
    volumes:
      - ./exports:/app/exports
      - ./data:/app/data
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: lead_user
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: lead_agent
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

Run:
```bash
docker-compose -f app/docker/docker-compose.yml up -d
```

## Cloud Deployment

### Render (Recommended)
1. Push to GitHub
2. Create new Web Service on Render
3. Set build command: `pip install -r app/requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Add environment variables (LLM_PROVIDER, LLM_API_KEY, DATABASE_URL)

### Heroku
```bash
# Install Heroku CLI
heroku login

# Create app
heroku create lead-capture-agent

# Set config
heroku config:set LLM_PROVIDER=mistral
heroku config:set LLM_API_KEY=your_key

# Deploy
git push heroku main
```

### AWS Lambda (with API Gateway)
1. Use AWS SAM or Serverless Framework
2. Create Lambda function with FastAPI
3. Use RDS for database
4. Set environment variables in Lambda config

### Google Cloud Run
```bash
gcloud run deploy lead-capture-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars "LLM_PROVIDER=mistral,LLM_API_KEY=your_key"
```

## Production Checklist

- [ ] Use PostgreSQL (not SQLite)
- [ ] Configure LLM API key securely
- [ ] Set up HTTPS/SSL
- [ ] Enable logging
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Add authentication (API keys/JWT)
- [ ] Set up automated backups
- [ ] Configure CORS properly (not `["*"]`)
- [ ] Use environment variables (not hardcoded)
- [ ] Set up CI/CD pipeline

## Scaling Considerations

### Single Instance
- Works for: 100-1000 leads/day
- Database: SQLite or small PostgreSQL
- LLM: Mistral/Gemini API

### Multiple Workers
- Works for: 1000-10,000 leads/day
- Use: PostgreSQL + Redis
- LLM: Mistral/Gemini (handle rate limits)
- Add: Load balancer (NGINX)

### Enterprise Scale
- Works for: 10,000+ leads/day
- Use: PostgreSQL cluster + Redis cluster
- LLM: Self-hosted Ollama instances
- Add: Message queue (RabbitMQ/Kafka)
- Add: Cache layer (Redis)
- Add: CDN for static assets

## Monitoring & Logging

### Application Logs
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Lead processed")
```

### Database Monitoring
```bash
# Check database size
SELECT pg_size_pretty(pg_database_size('lead_agent'));

# Count leads by quality
SELECT quality, COUNT(*) FROM leads GROUP BY quality;
```

### API Metrics
- Track request times
- Monitor error rates
- Alert on failures
- Dashboard (Grafana, DataDog)

## Backup Strategy

### Daily Exports
```bash
# Automated export script
*/6 * * * * python -c "from app.core.exporter import export_all_leads; from app.db.database import SessionLocal; export_all_leads(SessionLocal())"
```

### Database Backups
```bash
# PostgreSQL backup
pg_dump lead_agent > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql lead_agent < backup_20240115_100000.sql
```

## Troubleshooting

### High Memory Usage
- Check database connection pool
- Limit export size
- Use pagination for queries

### Slow LLM Responses
- Use faster model (mistral-small vs mistral-medium)
- Batch requests
- Implement caching

### Database Performance
- Add indexes on frequently queried columns
- Archive old leads
- Use read replicas

---

**Production-ready and scalable!**
