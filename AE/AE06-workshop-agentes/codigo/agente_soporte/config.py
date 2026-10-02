"""Configuración común: lee .env y crea el cliente LLM (API compatible con OpenAI)."""
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

RAIZ = Path(__file__).resolve().parent
load_dotenv(RAIZ / ".env")

LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:3b")
MAX_STEPS = int(os.getenv("AGENT_MAX_STEPS", "5"))
TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.1"))
DB_PATH = RAIZ / "deportienda.db"

cliente = OpenAI(base_url=os.getenv("LLM_BASE_URL"), api_key=os.getenv("LLM_API_KEY", "x"))
