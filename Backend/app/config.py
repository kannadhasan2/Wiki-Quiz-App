import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
APP_ENV = os.getenv("APP_ENV", "development").strip()

if not DATABASE_URL:
    raise RuntimeError("Missing DATABASE_URL in .env")
if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in .env")
