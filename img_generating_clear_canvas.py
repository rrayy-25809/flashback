from PIL import Image
import numpy as np
from collections import Counter

def canvas_clear() :
    new_image = Image.open("static/original_image.png")

    #캔버스 생상(이미지보다 크게)
    canvas_size = (3000, 1100)
    new_canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))

    #캔버스와 이미지의 중앙을 계산하여 이미지 중앙정렬
    new_image_size = new_image.size
    position = ((canvas_size[0] - new_image_size[0]) // 2, (canvas_size[1] - new_image_size[1]) // 2)

#새로운 이미지를 빈 캔버스에 붙이기
    new_canvas.paste(new_image, position, new_image.convert("RGBA"))

#이미지 저장
    new_output_path1 = "src/src.png"
    new_output_path2 = "src/mask.png"
    new_output_path3 = "src/sample.png"
    
    new_canvas.save(new_output_path1)
    new_canvas.save(new_output_path2)
    new_canvas.save(new_output_path3)

    new_output_path1
    new_output_path2
    new_output_path3
