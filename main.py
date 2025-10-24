from fastapi import FastAPI, HTTPException
from backend.news_api import fetch_news
from backend.database import init_db, save_news, get_news
from backend.scheduler import start_scheduler
from config import FREE_TRIAL_LIMIT, PAID_USERS

app = FastAPI(title="Lumina News KI")

# DB initialisieren
init_db()

# Scheduler starten
start_scheduler()

@app.get("/news")
def read_news(email: str, category: str = "general"):
    from backend.database import get_user_query_count
    if email not in PAID_USERS:
        if get_user_query_count(email) >= FREE_TRIAL_LIMIT:
            raise HTTPException(status_code=403, detail="Free Trial Limit erreicht")
    news_items = get_news(category)
    return {"category": category, "news":news_items}