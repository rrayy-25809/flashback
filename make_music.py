import requests
import os
from dotenv import load_dotenv
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
load_dotenv(verbose=True)
SUNO_AI_API_KEY=os.getenv('SUNO_AI_API_KEY')

url = "https://api.aimlapi.com/generate"
headers = {
    "Authorization": f"Bearer {SUNO_AI_API_KEY}",
    "Content-Type": "application/json"
}

def generate_music(prompt):
    payload = {
        "prompt": prompt,
        "make_instrumental": True,
        "wait_audio": True
    }
    response = requests.post(url, json=payload, headers=headers)

    #정상 출력돼었을때 (코드 200에서 300사이면 성공)
    if 200<= response.status_code <=299:
        json_data = json.loads(response.content)

        #json 형식에서 audio_url 만 가져와서 그 중 앞 링크 return
        for item in json_data: 
            item.get("audio_url"+",")
        output=item.get("audio_url")
        return output

    #아니라면
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        #defualt 값(500번 에러가 많이 발생하여)
        return "https://cdn.aimlapi.com/suno/99a82d0d-2f6a-4720-b25e-ad0e47a5ce63.mp3"
    
if __name__ == '__main__':  #C언어의 main 함수와 같은 개념의 조건문
    print(generate_music("create a healing music"))