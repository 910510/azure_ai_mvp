import os
from dotenv import load_dotenv

import requests

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

def discover_korean_tv_shows():
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }

    # TV SHOW GENRE
    genre_url = "https://api.themoviedb.org/3/genre/tv/list?language=ko"
    genre_response = requests.get(genre_url, headers=headers)
    genre_data = genre_response.json()
    genre_dict = {g['id']: g['name'] for g in genre_data.get("genres", [])}

    # TV SHOW
    url = "https://api.themoviedb.org/3/discover/tv"

    params = {
        "language": "ko-KR",                      # 한국어 응답
        "sort_by": "popularity.desc",              # 인기순 정렬
        "with_origin_country": "KR"               # 한국 제작 프로그램
    }

    tv_list = []

    for page in range(1, 6):
        params["page"] = page
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 에러 시 예외 발생

        data = response.json()
        results = data.get("results", [])
        if not results:
            print("No results found.")
        else:
            for item in results:
                if not item.get('overview'):
                        continue
                else:
                    genre = ''
                    for genre_id in item.get('genre_ids', []):
                        genre += genre_dict.get(genre_id, 'Unknown Genre') + ', '

                    tv_list.append({
                        "rank": len(tv_list) + 1,
                        "title": item.get('name', 'No title'),
                        "score": item.get('popularity', 'No score'),
                        "genre": genre.rstrip(', '),
                        "year": item.get('first_air_date', 'No year'),
                        "synopsis": item.get('overview', 'No synopsis')
                    })
    return tv_list

# 예시 실행
if __name__ == "__main__":
    korean_tv_shows = discover_korean_tv_shows()

    for idx, show in enumerate(korean_tv_shows, start=1):
        print(f"{idx}. {show['title']} ({show['year']})")
        print(f"   ⭐️ 평점: {show['score']} | 🔥 장르: {show['genre']}")
        print(f"   📖 {show['synopsis']}...\n")
