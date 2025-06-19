import os
import json
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "media")

client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(key))

def upload(json_path):
    with open(json_path, encoding="utf-8") as f:
        documents = json.load(f)
    result = client.upload_documents(documents=documents)
    print("✅ Upload result:", result)

if __name__ == "__main__":
    upload("embedding_for_aisearch.json")