import os
import requests
from PIL import Image
from io import BytesIO
import openai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 구성 설정
config = {
    "src_image_name": "src.png",
    "mask_image_name": "mask.png",
    "number_of_images": 1,
    "prompt": "high mountain",  # 여기에서 프롬프트를 입력하세요
    "src_folder_path": "./src",
    "rgba_folder_path": "./rgba",
    "dest_folder_path": "./dest",
}

# OpenAI API 초기화
openai.api_key = os.getenv("OPENAI_API_KEY")

# 유틸리티 함수
def convert_image_to_rgba(image_path, output_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGBA")
            img.save(output_path)
            print(f"{image_path}가 RGBA로 변환되었습니다.")
    except Exception as e:
        print(f"{image_path}를 RGBA로 변환하는 중 오류 발생: {e}")
        raise

def download_and_save_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"{url}에서 이미지가 성공적으로 다운로드되었습니다.")
    except Exception as e:
        print(f"{url}를 다운로드하는 중 오류 발생: {e}")
        raise

def check_and_create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"{folder_path} 폴더가 생성되었습니다.")

def process_images_with_openai(src_image, mask_image, prompt, n):
    try:
        print("이미지를 OpenAI로 전송 중... (몇 초 정도 소요됩니다)")
        response = openai.Image.create_edit(
            n=n,
            image=open(src_image, "rb"),
            mask=open(mask_image, "rb"),
            prompt=prompt,
        )
        return response["data"]
    except Exception as e:
        print(f"이미지를 OpenAI로 전송하는 중 오류 발생: {e}")
        raise

def validate_environment():
    if not openai.api_key:
        raise ValueError("OpenAI API 키가 .env 파일에서 찾을 수 없습니다.")
    
    if not (os.path.exists(f"{config['src_folder_path']}/{config['src_image_name']}") and
            os.path.exists(f"{config['src_folder_path']}/{config['mask_image_name']}")):
        raise ValueError("소스 이미지 또는 마스크 이미지가 존재하지 않습니다.")
    
    check_and_create_folder(config["rgba_folder_path"])
    check_and_create_folder(config["dest_folder_path"])
    
    src_image = Image.open(f"{config['src_folder_path']}/{config['src_image_name']}")
    mask_image = Image.open(f"{config['src_folder_path']}/{config['mask_image_name']}")
    
    if src_image.size != mask_image.size:
        raise ValueError("소스 이미지와 마스크 이미지의 해상도가 다릅니다.")

def resize_image(image_path, width, height):
    try:
        with Image.open(image_path) as img:
            img = img.resize((width, height))
            img.save(image_path)
            print(f"이미지가 {width}x{height}로 리사이즈되었습니다.")
    except Exception as e:
        print(f"이미지를 리사이즈하는 중 오류 발생: {e}")
        raise

# 핵심 함수
def image_processing():
    try:
        validate_environment()
        print("환경이 성공적으로 검증되었습니다.")
        
        rgba_src_image_path = f"{config['rgba_folder_path']}/_{config['src_image_name']}"
        rgba_mask_image_path = f"{config['rgba_folder_path']}/_{config['mask_image_name']}"
        
        convert_image_to_rgba(f"{config['src_folder_path']}/{config['src_image_name']}", rgba_src_image_path)
        convert_image_to_rgba(f"{config['src_folder_path']}/{config['mask_image_name']}", rgba_mask_image_path)
        
        images_data = process_images_with_openai(rgba_src_image_path, rgba_mask_image_path, config['prompt'], config['number_of_images'])
        
        output_filename = f"{config['dest_folder_path']}/outputimage.png"
        
        for idx, data in enumerate(images_data):
            download_and_save_image(data['url'], output_filename)
            print(f"{idx + 1}번째 이미지가 성공적으로 다운로드되었습니다.")
            
            # 이미지 크기 조정 (필요한 경우)
            resize_image(output_filename, 2048, 1024)
            
    except Exception as e:
        print(f"오류: {e}")
        return

def ask_user():
    while True:
        answer = input("이미지 처리를 시작하시겠습니까? (y/n): ").strip().lower()
        if answer == 'y':
            image_processing()
        else:
            print("프로그램이 종료되었습니다.")
            break

if __name__ == "__main__":
    ask_user()