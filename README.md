# Azure AI 기반 트렌드 VOD 추천 시스템

## 프로젝트 개요

이 프로젝트는 **Azure AI** 및 다양한 데이터 파이프라인을 활용하여, 유튜브 등에서 수집한 트렌드 기반 VOD(영화/드라마/예능) 데이터를 분석·가공하고, 이를 바탕으로 추천 및 질의응답 서비스를 제공하는 시스템입니다.

- **크롤러**: 트렌드/랭킹/뉴스 등 다양한 소스에서 데이터 수집
- **ML 파이프라인**: 데이터 정제, GPT 기반 요약/라벨링, 임베딩 생성, Azure AI Search 업로드
- **웹앱**: Azure OpenAI + AI Search 기반 RAG(검색증강생성) 챗봇 서비스

---

## 디렉토리 구조

```plaintext
.
├── app/
│   ├── crawler/                # 데이터 크롤러 (랭킹, 뉴스, TMDB 등)
│   ├── functions/
│   │   └── youtube/            # Azure Functions (유튜브 데이터 수집/처리)
│   └── webapp/                 # Streamlit 기반 챗봇 웹앱
├── ml_pipeline/
│   ├── scripts/                # 데이터 파이프라인 스크립트
│   ├── environments/           # Conda 환경 정의
│   └── deployments/            # Azure ML 파이프라인 정의
├── config.json                 # Azure 리소스 설정
├── requirements.txt            # 전체 의존성
├── pyproject.toml              # 프로젝트 메타정보
└── README.md                   # 프로젝트 설명서
```

---

## 주요 구성 요소 및 기능

### 1. 데이터 크롤러 (`app/crawler/`)

- **kinolights.py**: 키노라이츠 랭킹 크롤링 및 시놉시스 추출
- **naver_search.py, news.py**: 네이버 검색/뉴스 데이터 수집
- **tmdb_movie.py, tmdb_tv.py**: TMDB API를 통한 영화/TV 정보 수집
- **serpAPI.py**: Google SERP API 활용 검색 데이터 수집
- **utils.py**: 공통 유틸리티 함수

### 2. Azure Functions - 유튜브 데이터 파이프라인 (`app/functions/youtube/`)

- **youtube_scrapper.py**: 유튜브 API로 트렌드 영상 검색, 자막 추출, GPT 요약, Blob 업로드
- **logic.py**: 함수 실행 로직
- **trigger_http/**, **crawler_timer/**: HTTP 트리거/타이머 트리거 함수 정의
- **requirements.txt, host.json, local.settings.json**: 함수 앱 설정

### 3. 웹앱 (`app/webapp/`)

- **chat.py**: Streamlit 기반 RAG 챗봇 (Azure OpenAI + AI Search)
    - 유저 질문 → AI Search 문서 검색 → GPT 답변 생성
    - 트렌드 기반 VOD 추천/질의응답 제공
- **requirements.txt, run.sh**: 실행 및 의존성

### 4. ML 파이프라인 (`ml_pipeline/`)

#### [scripts/]
- **fetch_youtube_data.py**: 유튜브 트렌드 영상/자막 수집
- **clean_text.py**: 텍스트 정제 및 전처리
- **gpt_labeling.py**: GPT를 활용한 요약/라벨링
- **embedding_generate.py**: OpenAI 임베딩 생성
- **upload_to_aisearch.py**: 임베딩 결과를 Azure AI Search에 업로드

#### [environments/]
- **conda.yml, basic-env.yml**: 파이프라인 실행 환경 정의

#### [deployments/]
- **youtube_pipeline.yml**: 전체 데이터 파이프라인(Azure ML) 정의
    - 데이터 수집 → 정제 → GPT 요약 → 임베딩 → AI Search 업로드

---

## ML 파이프라인 상세 설명

본 프로젝트의 ML 파이프라인은 Azure Machine Learning을 활용하여 다음과 같은 단계로 구성됩니다:

1. **YouTube 데이터 수집**
    - `fetch_youtube_data.py`
    - 유튜브 API를 통해 트렌드/리뷰/추천 영상 및 자막 데이터를 수집합니다.
    - 결과: `youtube_raw_data.csv`

2. **텍스트 정제**
    - `clean_text.py`
    - 수집된 데이터(제목, 설명, 자막)를 소문자화, 특수문자 제거 등으로 정제합니다.
    - 결과: `cleaned_output.csv`

3. **GPT 요약 및 라벨링**
    - `gpt_labeling.py`
    - Azure OpenAI GPT를 활용해 각 영상의 요약, 장르, 분위기 등 라벨링 정보를 생성합니다.
    - 결과: `labeled_output.csv`

4. **임베딩 생성**
    - `embedding_generate.py`
    - 요약/라벨링된 텍스트를 OpenAI 임베딩 모델로 벡터화합니다.
    - 결과: `embedding_for_aisearch.json`

5. **Azure AI Search 업로드**
    - `upload_to_aisearch.py`
    - 생성된 임베딩 데이터를 Azure AI Search 인덱스에 업로드하여, 검색 기반 RAG 서비스에 활용합니다.

각 단계는 `ml_pipeline/deployments/youtube_pipeline.yml`에 정의되어 있으며, Azure ML Studio 또는 CLI를 통해 전체 파이프라인을 자동 실행할 수 있습니다.

---

## 설치 및 실행 방법

### 1. 환경 준비

```bash
# Python 3.11~3.12 권장
pip install -r requirements.txt
# 또는 poetry 사용 시
poetry install
```

### 2. 환경 변수 설정

- `.env` 파일 또는 `local.settings.json`에 Azure 및 API 키 정보 입력

### 3. 크롤러/파이프라인 실행

```bash
# 예시: 유튜브 데이터 수집 및 파이프라인 실행
python ml_pipeline/scripts/fetch_youtube_data.py
python ml_pipeline/scripts/clean_text.py --raw_input_path ... --output_path ...
python ml_pipeline/scripts/gpt_labeling.py --cleaned_data ... --output_path ...
python ml_pipeline/scripts/embedding_generate.py --labeled_data ... --output_path ...
python ml_pipeline/scripts/upload_to_aisearch.py
```

### 4. 웹앱 실행

```bash
cd app/webapp
streamlit run chat.py
```

---

## 환경 변수 예시 (.env)

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=https://your-openai-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_VERSION=2025-01-01-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your-embedding-deployment
AZURE_OPENAI_EMBEDDING_VERSION=2023-05-15

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://your-search-endpoint.search.windows.net/
AZURE_SEARCH_ADMIN_KEY=your-search-admin-key
AZURE_SEARCH_INDEX_NAME=media

# Youtube & 외부 API
YOUTUBE_API_KEY=your-youtube-api-key
TMDB_API_KEY=your-tmdb-api-key
SERP_API_KEY=your-serp-api-key
NEWS_API_KEY=your-news-api-key
NAVER_SEARCH_CLIENT_ID=your-naver-client-id
NAVER_SEARCH_CLIENT_SECRET=your-naver-client-secret
```

---

## 주요 기술 스택

- **Python 3.11~3.12**
- **Azure OpenAI, Azure AI Search, Azure ML**
- **Streamlit** (웹앱)
- **Selenium, BeautifulSoup, requests** (크롤러)
- **pandas, openai, youtube-transcript-api** (데이터 처리)