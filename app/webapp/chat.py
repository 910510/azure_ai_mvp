from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

import streamlit as st

import os
from dotenv import load_dotenv

load_dotenv()

search_client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"])
)

openai_client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_VERSION"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def run_rag_with_fallback(user_query: str) -> str:
    results = search_client.search(user_query, top=5)
    documents = [doc["content"] for doc in results if "content" in doc]

    if not documents:
        # Fallback: 문서 없이 사용자 질문만
        prompt = f"""
        문서 검색 결과가 없습니다.
        사용자 질문: "{user_query}"
        이 질문에 대해 일반적인 지식을 바탕으로 정중하게 답변해 주세요.
        """
    else:
        # 검색된 문서를 context로 사용
        context = "\n\n".join(documents)
        prompt = f"""
        당신은 문서 기반 질문 응답 도우미입니다.

        아래는 검색된 문서입니다:
        -------------------------
        {context}
        -------------------------

        사용자의 질문은 다음과 같습니다:
        "{user_query}"

        문서 내용을 최대한 반영하여 정확하고 친절하게 답변해 주세요.
        """

    # GPT 응답 생성
    response = openai_client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

st.title("Hello")

# if __name__ == "__main__":
#     query = input("질문을 입력하세요: ")
#     answer = run_rag_with_fallback(query)
#     print("\n📘 GPT 응답:")
#     print(answer)
