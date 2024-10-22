import os
import openai
from dotenv import load_dotenv
from transformers import CLIPProcessor, CLIPModel

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# CLIP 모델 및 프로세서 로드
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def ask_openai(description:str):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system", "content":"이미지를 분석하고 그 결과를 토대로 outpainting을 하는 역할이야"},
            {"role":"user", "content":f"{description}의 풍경은 어떨지 생각해봐. 그리고 우리에게 그것들을 명사만 나열해줘 개수는 10개 이하 "}
            #유저의 입력을 변수화하여 매개변수로 받아 프롬포트를 입력함 
        ],
        max_tokens=1000,
        temperature=0.1, #이미지 생성할때 인공지능의 창의성(높이니까 이상해짐)
        top_p=1, 
        n=1, #횟수
        stop=None,
    )
    answer = response.choices[0].message['content'].strip()
    return answer

if __name__ == "__main__": #C언어의 main 함수와 같은 개념의 조건문(테스트용)
    answer = ask_openai("")
    print(str(answer))