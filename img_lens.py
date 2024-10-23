import cv2
import numpy as np


def img_pano(file_name:str):
    # 이미지 파일 경로
    image_path = f'static/{file_name}_outpainted.jpg'  # 파노라마 효과를 적용할 이미지 경로
    image = cv2.imread(image_path)

    # Define the camera matrix for equirectangular projection
    K_360 = np.array([[image.shape[1], 0, image.shape[1] / 2],
                    [0, image.shape[1], image.shape[0] / 2],
                    [0, 0, 1]], dtype=np.float32)

    # Adjust the distortion coefficients for a moderate increase in barrel distortion
    D_moderate_barrel = np.array([-0.75, 0.3, 0, 0], dtype=np.float32)  # Moderately increased barrel distortion

    # Apply the moderate barrel distortion to the original image
    distorted_image = cv2.undistort(image, K_360, D_moderate_barrel)
    # 왜곡된 이미지 저장
    cv2.imwrite(f'static/{file_name}_pano.jpg', distorted_image)  # 저장 경로

    return f'static/{file_name}_pano.jpg'

if __name__ == '__main__':  #C언어의 main 함수와 같은 개념의 조건문
    img_pano("999")