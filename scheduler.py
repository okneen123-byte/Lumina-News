from apscheduler.schedulers.background import BackgroundScheduler
from backend.database import save_news
from config import UPDATE_INTERVAL_HOURS

def update_all_categories():
    categories = ["general", "technology", "business", "sports", "science", "entertainment"]
    for cat in categories:
        save_news(cat)
    print("News updated!")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_all_categories, "interval", hours=UPDATE_INTERVAL_HOURS)
    scheduler.start()