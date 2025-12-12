import os

# ----------------------------------------------------
# 1. 설정: 폴더 경로 설정
# ----------------------------------------------------

# 파일 이름 변경을 수행할 폴더 경로
TARGET_DIR = r"C:\dev\ItemTierList\item_images"

# ----------------------------------------------------
# 2. 메인 로직: 파일 이름 변경
# ----------------------------------------------------

def rename_files_in_folder():
    if not os.path.exists(TARGET_DIR):
        print(f"오류: 대상 폴더 경로를 찾을 수 없습니다: {TARGET_DIR}")
        return

    print(f"--- 폴더: {TARGET_DIR} 내 파일 이름 변경 시작 ---")
    
    count_renamed = 0
    
    # 폴더 내의 모든 파일과 폴더 목록을 가져옵니다.
    for filename in os.listdir(TARGET_DIR):
        # 파일 이름에 언더바('_')가 포함되어 있는지 확인합니다.
        if '_' in filename:
            
            # 언더바를 공백으로 치환하여 새 파일 이름을 만듭니다.
            new_filename = filename.replace('_', ' ')
            
            # 원본 파일의 전체 경로
            old_path = os.path.join(TARGET_DIR, filename)
            
            # 새 파일의 전체 경로
            new_path = os.path.join(TARGET_DIR, new_filename)
            
            # 파일인지 확인하고 이름 변경을 시도합니다.
            if os.path.isfile(old_path):
                try:
                    os.rename(old_path, new_path)
                    print(f"✅ 변경 완료: '{filename}' -> '{new_filename}'")
                    count_renamed += 1
                except Exception as e:
                    print(f"❌ 이름 변경 오류 ({filename}): {e}")
            
    print("\n--- 완료 ---")
    print(f"총 이름 변경 파일 수: {count_renamed}개")


if __name__ == "__main__":
    rename_files_in_folder()