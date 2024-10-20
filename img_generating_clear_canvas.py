from PIL import Image
import numpy as np
from collections import Counter

def canvas_clear() :
    new_image = Image.open("static/original_image.png")

    #캔버스 생상(이미지보다 크게)
    canvas_size = (3000, 1024)
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

def after_process_image(file_path: Image):
    new_image = Image.open(f"static/{file_path}.png")  
    new_image = fade_edges(new_image)  # 이미지의 가장자리를 흐리게 처리

    # 새로운 투명한 캔버스를 생성
    width, height = (2150, 1500)  # 캔버스의 크기 설정
    top_color, bottom_color = split_and_find_colors(new_image)  # 이미지에서 상단, 하단 색상을 추출
    new_canvas = Image.new("RGBA", (width, height))

    top_image = Image.new("RGB", (width, height // 2), top_color)  # 상단 색상으로 채운 이미지 생성
    bottom_image = Image.new("RGB", (width, height // 2), bottom_color)  # 하단 색상으로 채운 이미지 생성

    # 각각의 이미지를 위쪽과 아래쪽에 붙이기
    new_canvas.paste(top_image, (0, 0))  
    new_canvas.paste(bottom_image, (0, height // 2)) 

    # 캔버스 중앙에 새 이미지를 위치시키기 위한 좌표 계산
    new_image_size = new_image.size
    position = ((width - new_image_size[0]) // 2, (height - new_image_size[1]) // 2)  # 중앙 좌표 계산

    # 새 이미지를 투명한 캔버스 위에 붙이기
    new_canvas.paste(new_image, position, new_image.convert("RGBA"))
    
    new_output_path = f"static/{file_path}_faded.png"  
    new_canvas.save(new_output_path)




def fade_edges(img:Image, fade_width=10, fade_height=20):
    # 이미지 로드
    image = img.convert("RGBA")
    
    # 이미지 크기 가져오기
    width, height = image.size
    
    # 빈 마스크 만들기
    alpha = Image.new('L', (width, height), 255)
    
    # NumPy 배열로 변환
    alpha_np = np.array(alpha)
    
    # 왼쪽 페이드 인
    for x in range(fade_width):
        alpha_np[:, x] = (x / fade_width) * 255
    
    # 오른쪽 페이드 인
    for x in range(fade_width):
        alpha_np[:, width - x - 1] = (x / fade_width) * 255
    
    # 상부 페이드 인
    for y in range(fade_height):
        alpha_np[y, :] = np.minimum(alpha_np[y, :], (y / fade_height) * 255)
    
    # 하부 페이드 인 (추가)
    for y in range(fade_height):
        alpha_np[height - y - 1, :] = np.minimum(alpha_np[height - y - 1, :], (y / fade_height) * 255)
    
    # NumPy 배열을 다시 이미지로 변환
    alpha = Image.fromarray(alpha_np)
    
    # 원본 이미지에 알파 채널 추가
    image.putalpha(alpha)
    
    return image

def most_frequent_color(image_array):
    # RGB 값을 tuple로 변환
    pixels = [tuple(pixel) for row in image_array for pixel in row]
    
    # 가장 빈번한 색상을 찾기 위해 Counter 사용
    color_counter = Counter(pixels)
    most_common_color = color_counter.most_common(1)[0][0]
    
    return most_common_color

def split_and_find_colors(image, portion=0.2):  
    # 이미지를 numpy 배열로 변환
    image_array = np.array(image)
    
    # 이미지 높이의 절단 지점 계산 (위쪽과 아래쪽 각각 20% portion 변수 확인)
    cut_height = int(image_array.shape[0] * portion)
    
    # 위쪽과 아래쪽 부분으로 나누기
    top_part = image_array[:cut_height, :, :]
    bottom_part = image_array[-cut_height:, :, :]
    
    # 각각의 최다 색상 계산
    top_color = most_frequent_color(top_part)
    bottom_color = most_frequent_color(bottom_part)

    return top_color, bottom_color