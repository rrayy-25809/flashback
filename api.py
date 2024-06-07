import requests

api_key = "SG_d18f5a44d75e6033"
url = "https://api.segmind.com/v1/sd1.5-outpaint"
count = 0

def request_api(img:str, seed:int, position:int):
    global count
    # Request payload
    data = {
    "image": f"{img}",
    "prompt": "inside the building",
    "negative_prompt":"NONE",
    "scheduler": "DDIM",
    "num_inference_steps": 25,
    "img_width": 1024,
    "img_height": 1024,
    "scale": 1,
    "strength": 1,
    "offset_x": position,
    "offset_y": 0,
    "guidance_scale": 7.5,
    "mask_expand": 8,
    "seed": f"{seed}"
    }

    response = requests.post(url, json=data, headers={'x-api-key': api_key})

    # Check if the response is successful
    if response.status_code == 200:
        count+=1
        file_path = f"static/outpainted_image_{count}.jpg"
        with open(file_path, "wb") as img_file:
            img_file.write(response.content)
        print(f"Image saved as {file_path}")
        return file_path
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response Text:", response.text)
        return None
    
def reset_count():
    global count
    count = 0