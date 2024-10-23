import numpy as np
from PIL import Image
from collections import Counter

def find_color(file_name:str):
    img = Image.open(f'static/{file_name}_outpainted.png')
    r,g,b = split_and_find_colors(img)
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

def split_and_find_colors(image:Image, portion=0.2):  
    # 이미지를 numpy 배열로 변환
    image_array = np.array(image)
    
    # 이미지 높이의 절단 지점 계산 (위쪽과 아래쪽 각각 20% portion 변수 확인)
    cut_height = int(image_array.shape[0] * portion)
    
    # 위쪽과 아래쪽 부분으로 나누기
    top_part = image_array[:cut_height, :, :]
    # bottom_part = image_array[-cut_height:, :, :]
    
    # 각각의 최다 색상 계산
    top_color = most_frequent_color(top_part)
    # bottom_color = most_frequent_color(bottom_part)
    return top_color

def most_frequent_color(image_array):
    # RGB 값을 tuple로 변환
    pixels = [tuple(pixel) for row in image_array for pixel in row]
    
    # 가장 빈번한 색상을 찾기 위해 Counter 사용
    color_counter = Counter(pixels)
    most_common_color = color_counter.most_common(1)[0][0]
    
    return most_common_color