import os  # 파일 경로 확인을 위한 os 모듈

def validate_image_path(image_path, label):
    """ 이미지 경로가 유효한지 확인하고, 없으면 None 반환 """
    if image_path and not os.path.exists(image_path):
        print(f"⚠️ 경고: '{image_path}' 경로에 {label} 이미지 파일이 존재하지 않습니다. 기본 사각형이 사용됩니다.")
        return None
    return image_path