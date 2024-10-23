import cv2
import numpy as np


def img_pano(file_name:str):
    # 이미지 파일 경로
    image_path = f'/static/{file_name}_outpainted.png'  # 파노라마 효과를 적용할 이미지 경로
    image = cv2.imread(image_path)

    # 이미지의 높이와 너비를 가져오기
    height, width = image.shape[:2]

    # 카메라 매트릭스 정의
    camera_matrix = np.array([[width, 0, width // 2],
                            [0, width, height // 2],
                            [0, 0, 1]], dtype=np.float32)

    # 파노라마 렌즈 왜곡 계수 정의
    distortion_coefficients = np.array([-2.0, 0.8, 0, 0, 0], dtype=np.float32)  # k1, k2

    # 파노라마 왜곡 적용
    distorted_image = cv2.undistort(image, camera_matrix, distortion_coefficients)

    # 왜곡된 이미지 저장
    cv2.imwrite(f'/static/{file_name}_pano.jpg', distorted_image)  # 저장 경로
    
    return f'/static/{file_name}_pano.jpg'