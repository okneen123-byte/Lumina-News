import sqlite3
from backend.news_api import fetch_news

DB_NAME = "backend/news.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tabelle für News
    c.execute("""CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    title TEXT,
                    description TEXT,
                    url TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                 )""")
    # Tabelle für User-Abfragen
    c.execute("""CREATE TABLE IF NOT EXISTS user_queries (
                    email TEXT,
                    count INTEGER DEFAULT 0,
                    last_query DATE
                 )""")
    conn.commit()
    conn.close()

def save_news(category):
    news_items = fetch_news(category)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for item in news_items:
        c.execute("INSERT INTO news (category, title, description, url) VALUES (?, ?, ?, ?)",
                  (category, item["title"], item["description"], item["url"]))
    conn.commit()
    conn.close()

def get_news(category):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT title, description, url FROM news WHERE category=? ORDER BY timestamp DESC", (category,))
    rows = c.fetchall()
    conn.close()
    news_list = [{"title": r[0], "description": r[1], "url": r[2]} for r in rows]
    return news_list

def get_user_query_count(email):
    import datetime
    today = datetime.date.today()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT count, last_query FROM user_queries WHERE email=?", (email,))
    row = c.fetchone()
    if row:
        count, last_query = row
        last_query = datetime.datetime.strptime(last_query, "%Y-%m-%d").date()
        if last_query < today:
            count = 0
        c.execute("UPDATE user_queries SET count=? , last_query=? WHERE email=?", (count+1, today, email))
    else:
        count = 1
        c.execute("INSERT INTO user_queries (email, count, last_query) VALUES (?, ?, ?)", (email, count, today))
    conn.commit()
    conn.close()
    return count