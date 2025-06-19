import os
from dotenv import load_dotenv

import requests

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

def get_tmdb_popular_movies():
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }

    # MOVIE GENRE
    genre_url = "https://api.themoviedb.org/3/genre/movie/list?language=ko"
    genre_response = requests.get(genre_url, headers=headers)
    genre_data = genre_response.json()
    genre_dict = {g['id']: g['name'] for g in genre_data.get("genres", [])}

    url = "https://api.themoviedb.org/3/movie/popular?language=ko-KR&page="

    params = {
        "language": "ko-KR"
    }

    movie_list = []

    for page in range(1, 6):
        params["page"] = page

        response = requests.get(f"{url}{page}", headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching data from TMDB: {response.status_code}")
            break

        data = response.json()
        results = data.get('results', [])
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

                    movie_list.append({
                        "rank": len(movie_list) + 1,
                        "title": item.get('title', 'No title'),
                        "score": item.get('popularity', 'No score'),
                        "genre": genre.rstrip(', '),
                        "year": item.get('release_date', 'No year'),
                        "synopsis": item.get('overview', 'No synopsis')
                    })

    return movie_list

if __name__ == "__main__":
    movie_list = get_tmdb_popular_movies()

    for idx, movie in enumerate(movie_list, start=1):
        print(f"{idx}. {movie['title']} ({movie['year']})")
        print(f"   ⭐️ 평점: {movie['score']} | 🔥 장르: {movie['genre']}")
        print(f"   📖 {movie['synopsis']}...\n")