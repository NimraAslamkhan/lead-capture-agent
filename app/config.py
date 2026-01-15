import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mistral")  # mistral, gemini, or ollama
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "mistral-small-latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./leads.db")
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"

# Lead Scoring Thresholds
HOT_LEAD_THRESHOLD = 60
WARM_LEAD_THRESHOLD = 40

# Export Configuration
EXPORT_PATH = os.getenv("EXPORT_PATH", "./exports")
