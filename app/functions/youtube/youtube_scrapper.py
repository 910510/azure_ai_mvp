import os
import requests
import time
import csv
import logging

from datetime import datetime, timedelta
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

from azure.storage.blob import BlobServiceClient

# import argparse
# import pandas as pd

from openai import AzureOpenAI

from dotenv import load_dotenv

load_dotenv()

### Environment
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

### Azue OpenAI
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

## Init OpenAI Client
client = AzureOpenAI(
    api_version=AZURE_OPENAI_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

## Search Youtube API
def search_youtube_recent_nonshorts(query, region="KR", max_results=10):
    logging.info("search_youtube_recent_nonshorts")
    logging.info(f"query={query}")

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
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    logging.info(f"Youtube Search API Response={response}")
    data = response.json()

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

### Get Transcript To Youtube API Result
def get_transcript(video_id, lang="ko"):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        return " ".join([entry["text"] for entry in transcript])
    except NoTranscriptFound:
        return "[자막 없음]"
    except Exception as e:
        return f"[에러: {str(e)}]"

### GPT Labeling
prompt_template = """
제목: {title}
설명: {description}
스크립트:
{transcript}

위 콘텐츠의 제목/설명/스크립트를 바탕으로 다음 질문에 답해주세요:
- 이 콘텐츠는 어떤 종류의 콘텐츠를 설명하고 있나요? (예: 영화, 드라마, 예능)
- 이 콘텐츠가 설명하려 하는 콘텐츠의 제목은 무엇일까요? (예: 영화 제목, 드라마 제목, 예능 프로그램명)
- 이 콘텐츠가 설명하려 하는 콘텐츠의 분위기는 어떤가요? (예: 드라마의 경우 감정적인, 예능의 경우 유쾌한 등)
- 이 콘텐츠의 전체적인 요약은 어떻게 될까요? (예: 영화의 줄거리, 드라마의 주요 사건, 예능의 주요 에피소드 등)

답변은 한글로 주세요.
"""
def build_prompt(row):
    return prompt_template.format(
        title=row["title"],
        description=row["description"],
        transcript=row["transcript"][:1500]
    )

def call_gpt(prompt, retries=1):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content" : prompt
                    }
                ],
                max_tokens=4096,
                temperature=1.0,
                top_p=1.0,
                model=AZURE_OPENAI_DEPLOYMENT
            )
            print(response)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Retry {attempt+1}: {e}")
            logging.error(f"Error: {e}")
            time.sleep(2)
    return "GPT 호출 실패"

def save_to_csv(items, filename):
    logging.info("Start save_to_csv!")
    logging.info(f"items={items}")

    try:
        datas = []
        for item in items:
            datas.append({
                "title": item["title"],
                "gpt_summary": item["gpt_summary"]
            })

        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "gpt_summary"])
            writer.writeheader()
            for data in datas:
                writer.writerow(data)
    except Exception as e:
        logging.error(f"Error: {e}")

def upload_csv_to_blob(local_path, container, blob_name, conn_str):
    logging.info("Start upload_csv_to_blob!")
    logging.info(f"local_path={local_path}")

    blob_service = BlobServiceClient.from_connection_string(conn_str)
    container_client = blob_service.get_container_client(container)

    try:
        container_client.create_container()
    except Exception:
        pass  # 이미 있으면 무시

    blob_client = container_client.get_blob_client(blob_name)

    with open(local_path, "rb") as f:
        blob_client.upload_blob(f, overwrite=True)
