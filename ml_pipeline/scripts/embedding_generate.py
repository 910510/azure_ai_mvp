import os
import openai
import pandas as pd
import json
import time
import argparse

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_version = os.getenv("AZURE_OPENAI_EMBEDDING_VERSION")
embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

def embed_text(text, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = openai.Embedding.create(
                input=text,
                engine=embedding_deployment
            )
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Embedding 실패 - 재시도 {attempt + 1}: {e}")
            time.sleep(2)
    return []

def main(input_path, output_path):
    df = pd.read_csv(input_path)
    print(f"총 {len(df)}개의 샘플을 임베딩합니다...")

    output = []
    for idx, row in df.iterrows():
        content = row.get("gpt_summary", "")
        if not content:
            continue
        vector = embed_text(content)
        output.append({
            "id": str(idx),
            "title": row.get("title", ""),
            "gpt_summary": content,
            "embedding": vector
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"✅ 저장 완료: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--labeled_data", required=True)
    parser.add_argument("--output_path", default="embedding_for_aisearch.json")
    args = parser.parse_args()
    main(args.labeled_data, args.output_path)