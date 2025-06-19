import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_SEARCH_KEYWORD = "영화|드라마|예능 +추천|리뷰|인기 -단편 -짧은 -shorts -short -쇼츠 -노래 -음악 -playlist -광고 -게임"

def get_trending_videos(max_results=50):
    published_after = (datetime.utcnow() - timedelta(days=1)).isoformat("T") + "Z"
    
    params = {
        "part": "snippet",
        "q": YOUTUBE_SEARCH_KEYWORD,
        "regionCode": "KR",
        "type": "video",
        "order": "viewCount",
        "videoDuration": "any",
        "publishedAfter": published_after,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    resp = requests.get(YOUTUBE_SEARCH_URL, params=params)
    return resp.json().get("items", [])

def fetch_transcript(video_id, lang="ko"):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        return " ".join([entry["text"] for entry in transcript])
    except NoTranscriptFound:
        return "[자막 없음]"
    except Exception as e:
        return f"[에러: {str(e)}]"

def fetch_and_save():
    results = get_trending_videos()
    records = []
    for item in results:
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        transcript = fetch_transcript(video_id)
        records.append({
            "video_id": video_id,
            "title": snippet["title"],
            "description": snippet["description"],
            "published_at": snippet["publishedAt"],
            "transcript": transcript
        })
    df = pd.DataFrame(records)
    df.to_csv("youtube_raw_data.csv", index=False)

if __name__ == "__main__":
    fetch_and_save()