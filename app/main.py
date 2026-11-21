from fastapi import FastAPI, HTTPException
from app.db import get_connection

app = FastAPI(title="Game Support System API", version="0.1.0")


@app.get("/")
def root():
    return {"status": "ok", "service": "Game Support System Backend"}


@app.get("/health/db")
def health_db():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name FROM roles ORDER BY id;")
                roles = [{"id": r[0], "name": r[1]} for r in cur.fetchall()]

                cur.execute("SELECT id, name, is_active FROM categories ORDER BY id;")
                categories = [
                    {"id": c[0], "name": c[1], "is_active": c[2]}
                    for c in cur.fetchall()
                ]

        return {
            "database": "connected",
            "roles": roles,
            "categories": categories,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")