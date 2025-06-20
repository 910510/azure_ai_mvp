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

## 주요 기술 스택

- **Python 3.11~3.12**
- **Azure OpenAI, Azure AI Search, Azure ML**
- **Streamlit** (웹앱)
- **Selenium, BeautifulSoup, requests** (크롤러)
- **pandas, openai, youtube-transcript-api** (데이터 처리)