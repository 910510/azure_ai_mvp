import os
from dotenv import load_dotenv
import streamlit as st
from openai import AzureOpenAI

load_dotenv()

### Environment
### OpenAI
AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT=os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_VERSION=os.getenv("AZURE_OPENAI_VERSION")
model_name = "gpt-4o-mini"

### AI Search
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version=AZURE_OPENAI_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a travel assistant that provides information on travel service available from Margie's Travel."
        }
    ]

for messages in st.session_state.messages:
    st.chat_message(messages["role"]).write(messages["content"])

def get_openai_response(messages):
    rag_params = {
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": AZURE_SEARCH_ENDPOINT,
                    "index_name": AZURE_SEARCH_INDEX_NAME,
                    "authentication": {
                        "type": "api_key",
                        "key": AZURE_SEARCH_ADMIN_KEY,
                    },
                    "query_type": "vector",
                    "embedding_dependency": {
                        "type": "deployment_name",
                        "deployment_name": AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
                    },
                }
            }
        ],
    }
    
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
        extra_body=rag_params
    )

    completion = response.choices[0].message.content
    return completion

if user_input := st.chat_input("Questions:"):
