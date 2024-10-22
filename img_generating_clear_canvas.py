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