import requests

url = "https://api.aimlapi.com/generate"
headers = {
    "Authorization": "Bearer de35b220fdf0450588dd4654e67fe191",
    "Content-Type": "application/json"
}
payload = {
    "prompt": "create a music that ",
    "make_instrumental": True,
    "wait_audio": True
}
response = requests.post(url, json=payload, headers=headers)
print(response.content)