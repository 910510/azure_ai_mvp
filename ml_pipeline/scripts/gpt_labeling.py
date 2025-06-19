import os
import argparse
import pandas as pd
from openai import AzureOpenAI
import time

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION")

endpoint = AZURE_OPENAI_ENDPOINT
deployment = AZURE_OPENAI_DEPLOYMENT
subscription_key = AZURE_OPENAI_API_KEY
api_version = AZURE_OPENAI_VERSION
model_name = "gpt-4o-mini"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

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
        title=row["clean_title"],
        description=row["clean_description"],
        transcript=row["clean_transcript"][:1500]
    )

def call_gpt(prompt, retries=3):
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
                model=deployment
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Retry {attempt+1}: {e}")
            time.sleep(2)
    return "GPT 호출 실패"

def main(input_path, output_path):
    df = pd.read_csv(input_path)
    df["gpt_summary"] = df.apply(lambda row: call_gpt(build_prompt(row)), axis=1)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleaned_data")
    parser.add_argument("--output_path")
    args = parser.parse_args()
    main(args.cleaned_data, args.output_path)
