import os
from dotenv import load_dotenv
import requests

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")

def fetch_popular_kdrama_news(query="인기 드라마", max_results=10):
    url = "https://serpapi.com/search"

    params = {
        "engine": "google_news",
        "q": query,
        "hl": "ko",               # 한글
        "gl": "kr",               # 지역: 한국
        "sort_by": "date",       # 최신순 정렬
        "api_key": SERP_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = []

    for news in data.get("news_results", [])[:max_results]:
        print(news)
        results.append({
            "title": news.get("title"),
            "snippet": news.get("snippet"),
            "link": news.get("link"),
            "source": news.get("source"),
            "published": news.get("date")
        })

    return results

# 사용 예
if __name__ == "__main__":
    articles = fetch_popular_kdrama_news("인기 영화|드라마", 10)
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   🔗 {article['link']}")
        print(f"   📰 {article['source']} | 📅 {article['published']}")
        print(f"   📝 {article['snippet']}\n")