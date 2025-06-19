import os
import requests
from datetime import datetime, timedelta
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube_recent_nonshorts(api_key, query, region="KR", max_results=10):
    url = "https://www.googleapis.com/youtube/v3/search"

    published_after = (datetime.utcnow() - timedelta(days=1)).isoformat("T") + "Z"

    params = {
        "part": "snippet",
        "q": query,
        "regionCode": region,
        "type": "video",
        "order": "viewCount",
        "videoDuration": "any",
        "publishedAfter": published_after,
        "maxResults": max_results,
        "key": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    print(f"검색어: {query}, 결과 수: {len(data.get('items', []))}")

    results = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        results.append({
            "title": snippet["title"],
            "description": snippet["description"],
            "publishedAt": snippet["publishedAt"],
            "videoId": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}"
        })

    return results

def get_transcript(video_id, lang="ko"):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        return " ".join([entry["text"] for entry in transcript])
    except NoTranscriptFound:
        return "[자막 없음]"
    except Exception as e:
        return f"[에러: {str(e)}]"

if __name__ == "__main__":
    api_key = YOUTUBE_API_KEY
    keyword = "영화|드라마|예능 +추천|리뷰|인기 -단편 -짧은 -shorts -short -쇼츠 -노래 -음악 -playlist -광고 -게임"
    # "검색어": 검색어 문구가 포함된 비디오를 검색
    # +: 반드시 포함되어야 하는 단어
    # -: 반드시 제외되어야 하는 단어
    # Intitle: 비디오 제목에만 검색어를 적용
    # Description: 비디오 설명에만 검색어를 적용
    # |: OR 연산자, 여러 검색어를 조합할 때 사용
    # (): 그룹화, 복잡한 검색어를 만들 때 사용
    # $: 특정 단어나 문구로 끝나는 비디오를 검색

    results = search_youtube_recent_nonshorts(api_key, keyword, max_results=10)

    for i, video in enumerate(results, 1):
        transcript = get_transcript(video["videoId"])
        print(f"{i}. {video['title']} ({video['publishedAt']})")
        print(f"   📜 설명: {video['description']}")
        print(f"   📅 {video['publishedAt']}")
        print(f"   🔗 {video['url']}")
        print(f"   📝 스크립트: {transcript[:100]}...\n")  # 자막 앞 100자만 미리보기
        print(f"       스크립트 길이: {len(transcript)}")
        print(f"{'-' * 100}")
