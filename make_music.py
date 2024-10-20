import requests
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)
SUNO_AI_API_KEY=os.getenv('SUNO_AI_API_KEY')

url = "https://api.aimlapi.com/generate"
headers = {
    "Authorization": f"Bearer {SUNO_AI_API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "prompt": "create a music that ",
    "make_instrumental": True,
    "wait_audio": True
}
response = requests.post(url, json=payload, headers=headers)
print(response.content)