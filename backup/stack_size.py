import requests
from bs4 import BeautifulSoup
import re
import os
import time
import json

# --- 파일 경로 설정 ---
INPUT_FILE = 'data.js'
OUTPUT_FILE = 'data_updated_v7.js'
BASE_URL = "https://metaforge.app/arc-raiders/database/item/"

# --- 1. 유틸리티 함수 ---

def name_to_slug(item_name):
    """
    아이템 이름을 Metaforge URL 슬러그 형식으로 변환합니다.
    """
    # 1. 소문자 변환 및 괄호와 내용 제거
    slug = item_name.lower()
    slug = re.sub(r'\([^)]*\)', '', slug).strip()
    # 2. 아포스트로피, 쉼표, 마침표, 따옴표 등을 제거
    slug = re.sub(r"[,'\"()\.,/]", '', slug) 
    # 3. 모든 공백을 하이픈으로 변환
    slug = re.sub(r'\s+', '-', slug)
    # 4. 연속된 하이픈 방지 및 시작/끝 하이픈 제거
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug

def scrape_stack_size_from_detail(slug):
    """
    개별 아이템 페이지에 접속하여 'Stack Size'를 추출합니다.
    사용자님이 지적해주신 형제(Sibling) 구조를 최우선으로 처리합니다.
    """
    url = f"{BASE_URL}{slug}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- 최종 파싱 로직 (V7) ---
        
        # 'Stack Size' 텍스트를 포함하는 모든 요소를 검색 (대소문자 무시)
        stack_labels = soup.find_all(lambda tag: tag.name in ['h5', 'div', 'span', 'p'] and re.search(r'Stack\s*Size', tag.text, re.IGNORECASE))
        
        for stack_label in stack_labels:
            # 1. 라벨의 **가장 가까운 다음 형제 요소**에서 값 추출 시도 (사용자님의 지적 구조: <div>Stack Size</div> <div>10</div>)
            next_element = stack_label.find_next_sibling()
            
            # 텍스트가 숫자인지 확인
            if next_element:
                text = next_element.text.strip().replace(',', '')
                if text.isdigit():
                    return int(text)
            
            # 2. 라벨의 부모(StatRow)에서 'StatValue' 클래스를 가진 요소 검색 (Power Rod와 같은 일반적인 구조)
            stat_row = stack_label.find_parent('div', class_=re.compile(r'StatRow|stat-group', re.IGNORECASE))
            if stat_row:
                stack_value_el = stat_row.find('div', class_=re.compile(r'StatValue|stat-value', re.IGNORECASE))
                if stack_value_el:
                    stack_text = stack_value_el.text.strip().replace(',', '')
                    if stack_text.isdigit():
                        return int(stack_text)
                        
        # 정보를 찾지 못하면 기본값 1을 반환합니다.
        return 1

    except requests.exceptions.RequestException:
        return 1
    except Exception:
        return 1

# --- 2. data.js 처리 함수 (재활용) ---

def get_item_list_from_js(content):
    """
    data.js 파일 내용에서 아이템 목록(JS 배열 문자열)을 파이썬 리스트로 변환합니다.
    """
    match = re.search(r'\[\s*(\{[\s\S]*?\})\s*\]', content, re.DOTALL)
    if not match:
        return None
    
    js_array_string = match.group(0).strip()
    json_like_string = re.sub(r'(\w+):\s*', r'"\1": ', js_array_string)
    json_like_string = re.sub(r',\s*\]', ']', json_like_string)
    
    try:
        return json.loads(json_like_string)
    except json.JSONDecodeError:
        return None

def process_and_update_data_js(input_file, output_file):
    """
    data.js를 처리하고 웹 스크래핑 후 결과를 새 파일에 저장하는 메인 함수입니다.
    """
    if not os.path.exists(input_file):
        print(f"Fatal Error: 입력 파일 '{input_file}'을 찾을 수 없습니다. 프로그램을 종료합니다.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        file_content = f.read()

    item_list = get_item_list_from_js(file_content)
    if not item_list:
        return

    print(f"총 {len(item_list)}개의 아이템에 대해 개별 페이지 스크래핑을 시작합니다. (페이지당 1초 딜레이 적용)")
    print("-" * 50)
    
    updated_items = []
    total_updated_count = 0
    
    start_time = time.time()
    
    # 2. 모든 아이템에 대해 상세 페이지 스크래핑 및 스택 값 업데이트
    for i, item in enumerate(item_list):
        item_name = item['name']
        
        # URL 슬러그 생성
        slug = name_to_slug(item_name)
        
        # 스택 크기 추출 (웹 요청)
        stack_size = scrape_stack_size_from_detail(slug)
        
        # 업데이트 여부 확인
        if item.get('stack', 0) != stack_size:
            total_updated_count += 1
        
        item['stack'] = stack_size
        
        # 진행 상황 출력
        elapsed = time.time() - start_time
        avg_time = elapsed / (i + 1) if (i + 1) > 0 else 0
        remaining_sec = avg_time * (len(item_list) - (i + 1))
        
        print(f"[{i+1:3}/{len(item_list)}] {item_name:50} -> Stack: {stack_size:2} (Slug: {slug}) | 남은 시간: {remaining_sec:.0f}s")
        
        updated_items.append(item)
        
        # 웹사이트에 부하를 줄이기 위해 딜레이 적용
        time.sleep(1) 


    # 3. 업데이트된 아이템 리스트를 JS 배열 문자열로 변환 (기존 형식 유지)
    item_strings = []
    for item in updated_items:
        item_string = (
            f"    {{ id: {item['id']:4}, stack: {item['stack']:2}, name: \"{item['name']}\", "
            f"price: {item['price']:5}, tier: \"{item['tier']}\", kr_name: \"{item['kr_name']}\" }}"
        )
        item_strings.append(item_string)
    
    # 최종 JS 배열 문자열 구성
    updated_content = (
        "const lootItems = [\n"
        + ",\n".join(item_strings)
        + "\n];\n"
    )

    # 4. 결과 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("-" * 50)
    print(f"✅ 최종 완료! 총 {total_updated_count}개의 아이템 스택 정보가 업데이트되었습니다.")
    print(f"결과 파일: '{output_file}'이 생성되었습니다.")
    print(f"총 소요 시간: {time.time() - start_time:.2f}초")


# ==========================================
# 실행
# ==========================================
if __name__ == "__main__":
    process_and_update_data_js(INPUT_FILE, OUTPUT_FILE)