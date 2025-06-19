from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import time
from datetime import datetime

from utils import save_to_csv

def get_synopsis_from_detail(driver, detail_url: str) -> str:
    driver.get(detail_url)
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    synopsis_tag = soup.select_one(".synopsis").select_one(".text")
    synopsis = synopsis_tag.get_text(strip=True) if synopsis_tag else "No synopsis found"
    
    return synopsis

def extract_ranking_content() -> list:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    driver.get("https://m.kinolights.com/ranking/kino")
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    ranking_items = []

    for item in soup.select(".ranking-item"):
        title_tag = item.select_one(".info__title")
        sub_title_tag = item.select_one(".info__subtitle")
        score_tag = item.select_one(".score__number")
        link_tag = item.select_one("a")
    
        rank = item.index
        title = title_tag.get_text(strip=True) if title_tag else ""
        sub_title = sub_title_tag.get_text(strip=True) if sub_title_tag else ""
        score = score_tag.get_text(strip=True) if score_tag else ""
        link = link_tag['href'] if link_tag and link_tag.has_attr('href') else ""

        genre = sub_title.split(" · ")[0].strip() if sub_title else ""
        year = sub_title.split(" · ")[1].strip() if sub_title else ""

        if link:
            full_link = f"https://m.kinolights.com{link}" if link.startswith("/") else link

            synopsis = get_synopsis_from_detail(driver, full_link)

        if title:
            ranking_items.append({
                "rank": rank,
                "title": title,
                "score": score,
                "genre": genre,
                "year": year,
                "synopsis": synopsis
            })

    driver.quit()
    return ranking_items

if __name__ == "__main__":
    today_str = datetime.today().strftime("%Y%m%d")
    local_filename = f"kinolights_ranking_{today_str}.csv"
    blob_filename = f"ranking/{today_str}/kinolights_ranking.csv"

    content_list = extract_ranking_content()

    save_to_csv(content_list, local_filename)