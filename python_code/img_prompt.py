import os
# from PIL import Image #사용할때만 켜주세용
import openai
from dotenv import load_dotenv
from transformers import CLIPProcessor, CLIPModel

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# CLIP 모델 및 프로세서 로드
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# 이미지 로드
# img = Image.open("static/original_image.png") #보류

# by gpt
# def get_image_features(image):
#     # 이미지를 CLIP 입력 형식으로 변환
#     inputs = processor(images=image, return_tensors="pt")

#     # 이미지의 특징 벡터 추출
#     with torch.no_grad():
#         features = model.get_image_features(**inputs)
#     return features

def ask_openai():
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role":"system", "content":"이미지를 분석하고 그 결과를 토대로 outpainting을 하는 역할이야"},
            # {"role":"user", "content":f"이미지를 분석하고 이 이미지가 어떤 곳에 있는 이미지인지 생각하고 출력해. 그 후 이 이미지를 outpainting 해야하는데 너가 분석한 이미지의 특징을 토대로 이미지를 outpainting 할 때 주변에 무엇이 있어야하는지 단어로. 그 단어만 이야기해. 이미지를 분석하고, 이미지의 요소를 파악한 후 이미지 주변에 어떤 풍경이 있어야 좋을지 판단해서 보내. 너무 여러개를 뽑을 생각 하지 말고 원본 이미지에 더 기반해서 말해: {imgs}"},
            # 위: 이미지로 생성할 떄 쓰는 코드
            {"role":"user", "content":f"초겨울 그러니까 하늘은 높고 춥긴 하지만 눈은 없는 설악산 대청봉의 풍경은 어떨지 생각해봐. 그리고 우리에게 그것들을 명사만 나열해줘 개수는 10개 이하 "}
            #앞 문장은 사용자가 웹사이트에서 입력받은 문자열을 그대로 붙어넣을꺼임-> 변수화 하겠다는 말
        ],
        max_tokens=1000,
        temperature=0.1, #너무 높이니까 이상해짐
        top_p=1, 
        n=1, #횟수
        stop=None,
    )
    answer = response.choices[0].message['content'].strip()
    return answer

def main():
        # features = get_image_features(img)
        answer = ask_openai()
        print(f"{answer}")


if __name__ == "__main__":
    main()  