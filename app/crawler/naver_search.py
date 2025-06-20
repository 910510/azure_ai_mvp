import os
import requests
from dotenv import load_dotenv

load_dotenv()

NAVER_SEARCH_CLIENT_ID = os.getenv("NAVER_SEARCH_CLIENT_ID")
NAVER_SEARCH_CLIENT_SECRET = os.getenv("NAVER_SEARCH_CLIENT_SECRET")

url = ('https://openapi.naver.com/v1/search/news.json?'
        'query=%EC%A3%BC%EC%8B%9D'
        'display=10'
        'start=1'
        'sort=sim'
        f'-H "X-Naver-Client-Id: {NAVER_SEARCH_CLIENT_ID}'
        f'-H "X-Naver-Client-Secret: {NAVER_SEARCH_CLIENT_SECRET}'
    )

response = requests.get(url)

print(response.json())