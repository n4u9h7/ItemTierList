import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extract_arc_loot_list():
    url = "https://metaforge.app/arc-raiders/loot-value-tiers"
    
    # 브라우저 설정
    options = Options()
    options.add_argument("--headless")  # 화면 없이 실행
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"페이지 접속 중: {url}")
        driver.get(url)
        time.sleep(5)  # 초기 로딩 대기

        # 모든 데이터를 로드하기 위해 끝까지 스크롤
        print("모든 아이템 로드 중 (스크롤)...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # 아이템 행(Row) 추출
        # MetaForge의 구조상 아이템 이름, 가격을 포함하는 요소를 탐색합니다.
        items = driver.find_elements(By.XPATH, "//div[contains(@class, 'flex')]//div[contains(@class, 'flex-col')]")
        
        loot_list = []
        item_id = 1
        
        # 중복 제거를 위한 세트
        seen_names = set()

        # 페이지 내 텍스트 정보를 기반으로 데이터 정제
        # 실제 사이트의 CSS 클래스 구조를 기반으로 텍스트를 파싱합니다.
        raw_text = driver.find_element(By.TAG_NAME, "body").text
        # 정규표현식: 아이템명과 숫자(가격)가 연속되는 패턴 추출 시도
        lines = raw_text.split('\n')
        
        current_name = None
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # 가격(숫자)인 경우 이전 줄의 이름과 결합
            if line.isdigit() and current_name:
                price = int(line)
                if current_name not in seen_names:
                    # 티어 결정 로직
                    if price >= 5000: tier = "S"
                    elif price >= 3000: tier = "A"
                    elif price >= 1200: tier = "B"
                    elif price >= 800: tier = "C"
                    else: tier = "D"
                    
                    loot_list.append({
                        "id": item_id,
                        "name": current_name,
                        "price": price,
                        "tier": tier
                    })
                    seen_names.add(current_name)
                    item_id += 1
                current_name = None
            else:
                # 무시할 단어 필터링
                if line not in ["Sell Price", "Weight", "ARC Raiders", "Loot Value Tiers"]:
                    current_name = line

        # 결과를 txt 파일로 저장 (Javascript 배열 형식)
        with open("loot_list.txt", "w", encoding="utf-8") as f:
            f.write("const baseItems = [\n")
            for i, item in enumerate(loot_list):
                comma = "," if i < len(loot_list) - 1 else ""
                f.write(f'    {{ id: {item["id"]}, name: "{item["name"]}", price: {item["price"]}, tier: "{item["tier"]}" }}{comma}\n')
            f.write("];")
            
        print(f"완료! 총 {len(loot_list)}개의 아이템이 loot_list.txt에 저장되었습니다.")

    finally:
        driver.quit()

if __name__ == "__main__":
    extract_arc_loot_list()