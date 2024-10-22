from PIL import Image

def canvas_clear() :
    new_image = Image.open("static/original_image.png")

    # 캔버스 크기(이미지보다 크게 설정)
    canvas_size = (1024, 512)
    new_canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))

    # 이미지의 크기 계산
    new_image_size = new_image.size
    # 이미지를 왼쪽 정렬하고, 세로는 중앙 정렬
    position = ((canvas_size[0] - new_image_size[0]) // 2, (canvas_size[1] - new_image_size[1]) // 2)

    # 이미지를 빈 캔버스에 붙이기
    new_canvas.paste(new_image, position, new_image.convert("RGBA"))

    # 이미지 저장 경로 설정
    new_output_path1 = "src/src.png"
    new_output_path2 = "src/mask.png"
    new_output_path3 = "src/sample.png"
    
    new_canvas.save(new_output_path1)
    new_canvas.save(new_output_path2)
    new_canvas.save(new_output_path3)

    return new_output_path1, new_output_path2, new_output_path3





def second_canvas(file_name: str):
    image = Image.open(f"static/{file_name}.png")
    w, h = image.size

    # 왼쪽 600픽셀을 자른 이미지
    left_cropped = image.crop((0, 0, 600, h))
    left_cropped.save(f"static/left_cropped_{file_name}.png")
    
    # 오른쪽 600픽셀을 자른 이미지
    right_cropped = image.crop((w, 0, w - 600, h))
    right_cropped.save(f"static/right_cropped_{file_name}.png")
    
    canvas_size = (1800, h)
    new_canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))

    # 이미지를 왼쪽 정렬하고, 세로는 중앙 정렬
    position_left =(0,1200) 
    position_right = (0,0)
    # 이미지를 빈 캔버스에 붙이기
    new_canvas.paste(left_cropped, position_left, image.convert("RGBA"))
    new_canvas.paste(right_cropped, position_right, image.convert("RGBA"))

    # 이미지 저장 경로 설정
    new_output_path1 = "src/src1.png"
    new_output_path2 = "src/mask1.png"
    new_output_path3 = "src/sample1.png"
    
    new_canvas.save(new_output_path1)
    new_canvas.save(new_output_path2)
    new_canvas.save(new_output_path3)

    return new_output_path1, new_output_path2, new_output_path3
