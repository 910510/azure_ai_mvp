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
        "{'position': 1, 'title': '4화만에 ‘세계 1위’ 차지하며 해외에서 인기 급상승중인 한국 드라마', "
        "'source': {'name': 'MSN', 'icon': 'https://encrypted-tbn2.gstatic.com/faviconV2?url=https://www.msn.com&client=NEWS_360&size=96&type=FAVICON&fallback_opts=TYPE,SIZE,URL'}, "
        "'link': 'https://www.msn.com/ko-kr/news/other/4%ED%99%94%EB%A7%8C%EC%97%90-%EC%84%B8%EA%B3%84-1%EC%9C%84-%EC%B0%A8%EC%A7%80%ED%95%98%EB%A9%B0-%ED%95%B4%EC%99%B8%EC%97%90%EC%84%9C-%EC%9D%B8%EA%B8%B0-%EA%B8%89%EC%83%81%EC%8A%B9%EC%A4%91%EC%9D%B8-%ED%95%9C%EA%B5%AD-%EB%93%9C%EB%9D%BC%EB%A7%88/ar-AA1H3w89', "
        "'thumbnail': 'https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AA1H3w6X.img?w=658&h=370&m=6&x=338&y=121&s=85&d=85', "
        "'thumbnail_small': 'https://news.google.com/api/attachments/CC8iI0NnNTFlSGxKUTNobWQwVmhkekJUVFJEeUFoaVNCU2dLTWdB', "
        "'date': '06/20/2025, 12:09 AM, +0000 UTC'}"
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