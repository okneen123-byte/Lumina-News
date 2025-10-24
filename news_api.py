import requests
from config import NEWS_API_KEY

def fetch_news(category="general"):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={NEWS_API_KEY}&language=en"
    response = requests.get(url)
    data = response.json()
    news_items = []
    for article in data.get("articles", []):
        news_items.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"]
        })
    return news_items