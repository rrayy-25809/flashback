# RE:mind 🎗️ - FLASHBACK

## 알고리즘
1. 유저에게서 원본 사진과 사진의 특징을 입력하면 chat gpt api를  사용하여 자동으로 prompt를 생성.

2. 입력받은 파일을 확인하고 Pillow라이브러리를 통해 해상도 조정.

3. 조정된 사진은 static폴더에 저장되고 img_generating_clear_canvas.py에서 투명 캔버스를 포함한 더 큰 해상도의 사진으로 변환.

4. 변환된 사진은 chat gpt api를 이용하여 outpainting됨.

5. outpainting이 된 파일은 static폴더에 저장되고 이 파일을 html파일에서 읽음.

6. 읽어진 파일은 A-Frame 프레임워크로 가상환경을 만들고 병합된 이미지를 사용하여 VR로 볼 수 있게 표현.


## 앱
(현재 스윙투앱을 사용하여 웹앱을 제작)