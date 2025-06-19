import logging
import os
from datetime import datetime
from youtube_scrapper import search_youtube_recent_nonshorts, get_transcript, call_gpt, build_prompt, save_to_csv, upload_csv_to_blob

def run_logic():
    logging.info("Azure Function Youtube Scrapper Start!")

    keyword = "영화|드라마|예능 +추천|리뷰|인기 -단편 -짧은 -shorts -short -쇼츠 -노래 -음악 -playlist -광고 -게임"
    # "검색어": 검색어 문구가 포함된 비디오를 검색
    # +: 반드시 포함되어야 하는 단어
    # -: 반드시 제외되어야 하는 단어
    # Intitle: 비디오 제목에만 검색어를 적용
    # Description: 비디오 설명에만 검색어를 적용
    # |: OR 연산자, 여러 검색어를 조합할 때 사용
    # (): 그룹화, 복잡한 검색어를 만들 때 사용
    # $: 특정 단어나 문구로 끝나는 비디오를 검색

    data = search_youtube_recent_nonshorts(keyword, max_results=50)
    logging.info(f"Youtube Search API Complete, data: {len(data)}")

    result = []
    for i, video in enumerate(data, 1):
        video["transcript"] = get_transcript(video["videoId"])
        video["gpt_summary"] = call_gpt(build_prompt(video))
        if video["gpt_summary"]:
            result.append(video)
    
    logging.info(f"GPT Labelling Complete, result: {len(result)}")

    today_str = datetime.today().strftime("%Y-%m-%d")
    filename = f"/tmp/youtuabe_{today_str}.csv"
    blob_path = f"{today_str}/youtube_ranking.csv"

    save_to_csv(result, filename)

    conn_str = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    container = os.environ.get("AZURE_STORAGE_CONTAINER", "ranking")

    upload_csv_to_blob(filename, container, blob_path, conn_str)

    logging.info("Azure Function Youtube Scrapper Complete!")