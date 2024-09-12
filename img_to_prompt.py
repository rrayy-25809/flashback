import os
import openai
from dotenv import load_dotenv
from transformers import CLIPProcessor, CLIPModel
import base64

"""----------------THIS CODE IS FOR TEST----------------"""

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# CLIP 모델 및 프로세서 로드
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def ask_openai(image_path:str): # Path to your image
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system", "content":"이미지를 분석하고 그 결과를 토대로 outpainting을 하는 역할이야"},
            {"role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "What’s in this image?"
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encode_image(image_path)}"
                    }
                    }
                ]
            }
        ],
        max_tokens=300,
        temperature=0.1, #너무 높이니까 이상해짐
        top_p=1, 
        n=1, #횟수
        stop=None,
    )
    answer = response.choices[0].message['content'].strip()
    return answer

if __name__ == "__main__":#테스트를 위한 코드
    answer = ask_openai("static\original_image.png")
    print(f"{answer}")