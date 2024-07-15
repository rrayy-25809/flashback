# from PIL import Image
# import openai 
# from dotenv import load_dotenv
# import torch
# from transfomers import CLIPProcessor, CLIPModel
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
# img=Image.open("static/original_image.png")

# def ask_openai():
#     response=openai.Completion.create(
#     model="gpt-4o",
#     prompt="이미지를 분석하고 이 이미지가 어떤 곳에 있는 이미지인지 생각해 그 후 이 이미지를 outpainting 할꺼야 너가 분석한 자료를 토대로 이미지를 outpainting할 때 주변에 무엇이 있어야하는지 한문장으로 출력해 무조건 그 한문장만",
#     max_tokens=1000,
#     temperature=0.7,
#     top_p=1,
#     n=1,
#     stop=None,
#     )
#     answer=response.choices[0].text.strip()
#     return answer

# def main():
#     while True:
#         message=input("Message: ")
#         answer=ask_openai(message)
#         print(f"Answer:{answer}")
# if __name__== "__main__":
#     main()




import openai
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import os

# OpenAI API 키 설정
image_path = "static/original_image.png"
openai.api_key = os.getenv("OPENAI_API_KEY")
# CLIP 모델 및 프로세서 로드
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_image_features(image_path):
    # 이미지 로드
    image = Image.open(image_path)

    # 이미지를 CLIP 입력 형식으로 변환
    inputs = processor(images=image, return_tensors="pt")

    # 이미지의 특징 벡터 추출
    with torch.no_grad():
        features = model.get_image_features(**inputs)

    return features

def describe_image(image_path):
    # 이미지의 특징 벡터 추출
    features = get_image_features(image_path)
    
    # 특징 벡터를 텍스트로 변환
    description = openai.Completion.create(
        engine="text-davinci-003",
        # engine="got-4o",
        prompt=f"Describe the image with features: {features}",
        max_tokens=100
    )

    return description.choices[0].text.strip()

# 이미지 파일 경로

# 이미지 설명 출력
description = describe_image(image_path)
print("Image Description:", description)
