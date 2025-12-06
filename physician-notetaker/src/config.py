import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    TEMPERATURE = 0
    MAX_TOKENS = 2048

    # JSON mode configuration
    RESPONSE_FORMAT = {"type": "json_object"}  # Forces JSON output
