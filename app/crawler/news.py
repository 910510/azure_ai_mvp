import os
from dotenv import load_dotenv
import requests

load_dotenv

url = ('https://newsapi.org/v2/everything?'
       'q=한국 인기 영화&'
       'from=2025-06-10&'
       'sortBy=popularity&'
       f'apiKey={os.getenv("NEWS_API_KEY")}')

response = requests.get(url)

print(response.json())