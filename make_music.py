import requests
import os
from dotenv import load_dotenv
import json
load_dotenv(verbose=True)
SUNO_AI_API_KEY=os.getenv('SUNO_AI_API_KEY')

url = "https://api.aimlapi.com/generate"
headers = {
    "Authorization": f"Bearer {SUNO_AI_API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "prompt": "create a healing music ",
    "make_instrumental": True,
    "wait_audio": True
}
response = requests.post(url, json=payload, headers=headers)

if 200<= response.status_code <=299:
    json_data = json.loads(response.content)
    for item in json_data:
        item.get("audio_url"+",")
    output=item.get("audio_url")
    output.split(",")
    print(output[1])
else:
    print(f"Failed with status code: {response.status_code}")
    print(response.text)
    