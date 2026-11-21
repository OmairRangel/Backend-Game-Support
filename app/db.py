import os
from pathlib import Path
from urllib.parse import quote_plus, urlparse, urlunparse
from dotenv import load_dotenv
import psycopg

BASE_DIR = Path(__file__).resolve().parent.parent


def _normalize_db_url(raw_url: str) -> str:
    parsed = urlparse(raw_url)
    if parsed.username and parsed.password is not None:
        safe_password = quote_plus(parsed.password)
        netloc = f"{parsed.username}:{safe_password}@{parsed.hostname}"
        if parsed.port:
            netloc += f":{parsed.port}"
        return urlunparse(parsed._replace(netloc=netloc))
    return raw_url


def get_connection():
    load_dotenv(BASE_DIR / ".env", override=True)
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set in .env")
    normalized_url = _normalize_db_url(db_url)
    return psycopg.connect(normalized_url, sslmode="require")