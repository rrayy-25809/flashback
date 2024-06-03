import requests

api_key = "SG_d18f5a44d75e6033"
url = "https://api.segmind.com/v1/sd1.5-outpaint"

def request_api(img:str):
    # Request payload
    data = {
    "image": f"{img}",
    "prompt": "inside the building",
    "negative_prompt":"NONE",
    "scheduler": "DDIM",
    "num_inference_steps": 25,
    "img_width": 1024,
    "img_height": 576,
    "scale": 1,
    "strength": 1,
    "offset_x": 256,
    "offset_y": 0,
    "guidance_scale": 7.5,
    "mask_expand": 8,
    "seed": 124567
    }

    response = requests.post(url, json=data, headers={'x-api-key': api_key})

    # Check if the response is successful
    if response.status_code == 200:
        # Save the response content as an image file
        with open("outpainted_image.jpg", "wb") as img_file:
            img_file.write(response.content)
        print("Image saved as outpainted_image.jpg")
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response Text:", response.text)