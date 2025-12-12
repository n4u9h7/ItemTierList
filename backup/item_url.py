import requests
from bs4 import BeautifulSoup
import time
import os
import re

# --- 설정 변수 ---
BASE_LIST_URL = "https://metaforge.app/arc-raiders/database/items/page/"
OUTPUT_FILE = 'item_urls_extracted_final.txt'
# 총 13페이지임을 알지만, 안전하게 15페이지까지 시도하여 끝까지 확인합니다.
MAX_PAGES = 15 

def extract_all_item_urls():
    """
    Metaforge의 모든 페이지 목록을 순회하며 아이템의 상세 페이지 URL을 추출합니다.
    HTML 구조에 상관없이 item/ 패턴을 가진 링크를 정규식으로 강력하게 검색합니다.
    """
    all_urls = set()  # 중복 제거를 위해 set 사용
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Metaforge 아이템 목록 페이지 스크래핑을 시작합니다. (최대 {MAX_PAGES}페이지)")
    print("-" * 50)
    
    for page_num in range(1, MAX_PAGES + 1):
        list_url = f"{BASE_LIST_URL}{page_num}"
        print(f"페이지 {page_num} 접속 시도 중... ({list_url})")
        
        try:
            response = requests.get(list_url, headers=headers, timeout=15)
            # HTTP 오류(404 포함) 발생 시 예외 처리
            response.raise_for_status() 
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- 핵심 로직: 정규식을 사용한 강력한 URL 패턴 검색 ---
            # 'href' 속성이 '/arc-raiders/database/item/'으로 시작하는 모든 <a> 태그를 찾습니다.
            links = soup.find_all('a', href=re.compile(r'/arc-raiders/database/item/'))
            
            page_url_count = 0
            
            for link in links:
                href = link['href']
                
                # 상대 경로인 경우 (e.g., /arc-raiders/database/item/snap-hook)
                if href.startswith('/'):
                    full_url = "https://metaforge.app" + href
                    # 아이템 상세 페이지 URL만 추가 (items/page/1 와 같은 목록 페이지 URL은 제외)
                    if not re.search(r'/item$', full_url) and not re.search(r'/items/page/\d+$', full_url):
                        all_urls.add(full_url)
                        page_url_count += 1
                
                # 절대 경로인 경우
                elif href.startswith('http') and 'metaforge.app/arc-raiders/database/item/' in href:
                    if not re.search(r'/item$', href) and not re.search(r'/items/page/\d+$', href):
                        all_urls.add(href)
                        page_url_count += 1


            print(f"-> 페이지 {page_num}에서 {page_url_count}개의 아이템 URL 추출 완료. (총 {len(all_urls)}개)")
            
            # 페이지에 아이템 링크가 없으면 목록이 끝난 것으로 간주하고 종료
            if page_url_count == 0 and page_num > 1:
                 print("-> 더 이상 아이템 링크가 발견되지 않아 스크래핑을 종료합니다.")
                 break
                 
            # 웹사이트에 부하를 줄이기 위해 딜레이 적용
            time.sleep(1) 
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404 and page_num > 1:
                print(f"-> 페이지 {page_num}은 존재하지 않습니다 (404). 모든 페이지 확인 완료.")
                break
            else:
                print(f"Error: HTTP 오류 발생 (상태 코드: {response.status_code}). 다음 페이지로 이동합니다.")
                time.sleep(2) 
                continue
        except requests.exceptions.RequestException as e:
            print(f"Error: 웹 접속 오류 발생: {e}. 다음 페이지로 이동합니다.")
            time.sleep(2) 
            continue
        except Exception as e:
            print(f"Error: 데이터 처리 중 오류 발생: {e}")
            break

    return all_urls

def save_urls_to_file(urls, filename):
    """
    추출된 URL 리스트를 파일에 저장합니다.
    """
    if not urls:
        print("경고: 추출된 URL이 없습니다. 파일 저장을 건너뜁니다.")
        return
        
    with open(filename, 'w', encoding='utf-8') as f:
        # 가독성을 위해 URL을 정렬하여 저장
        for url in sorted(list(urls)):
            f.write(url + '\n')
            
    print("-" * 50)
    print(f"✅ URL 추출 완료! 총 {len(urls)}개의 아이템 URL이 '{filename}'에 저장되었습니다.")
    

# ==========================================
# 실행
# ==========================================
if __name__ == "__main__":
    extracted_urls = extract_all_item_urls()
    save_urls_to_file(extracted_urls, OUTPUT_FILE)