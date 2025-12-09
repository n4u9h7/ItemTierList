import os
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def download_images_with_selenium():
    url = "https://metaforge.app/arc-raiders/loot-value-tiers"
    folder_name = "arc_raiders_images"

    # 폴더 생성
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 크롬 옵션 설정
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 화면 없이 실행하려면 주석 해제
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    # 드라이버 설치 및 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(5)  # 페이지 로딩 대기

        # 페이지 끝까지 스크롤 (Lazy Loading 이미지 로드 목적)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # 모든 img 태그 찾기
        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"발견된 전체 이미지 수: {len(images)}")

        download_count = 0
        for img in images:
            src = img.get_attribute("src")
            alt = img.get_attribute("alt") or f"item_{download_count}"
            
            # 아이템 관련 이미지만 필터링
            if src and ("/images/items/" in src or "metaforge.app" in src):
                # 특수문자 제거
                clean_name = re.sub(r'[\\/:*?"<>|]', '', alt).strip()
                file_path = os.path.join(folder_name, f"{clean_name}.webp")

                try:
                    img_data = requests.get(src, timeout=10).content
                    with open(file_path, 'wb') as f:
                        f.write(img_data)
                    print(f"다운로드 성공: {file_path}")
                    download_count += 1
                except Exception as e:
                    print(f"다운로드 실패 ({alt}): {e}")

        print(f"\n총 {download_count}개의 이미지를 다운로드했습니다.")

    finally:
        driver.quit()

if __name__ == "__main__":
    download_images_with_selenium()