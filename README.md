# RE:mind 🎗️ - FLASHBACK

## 사용된 개발환경
language

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Javascript-F7DF1E?style=flat-square&logo=javascript&logoColor=black"/> <img src="https://img.shields.io/badge/HTML-E34F26?style=flat-square&logo=html5&logoColor=white"/> <img src="https://img.shields.io/badge/CSS-3776AB?style=flat-square&logo=css3&logoColor=white"/>

librarys

<img src="https://img.shields.io/badge/Flask-3776AB?style=flat-square&logo=flask&logoColor=white"/> <img src="https://img.shields.io/badge/Aframe.js-EF2D5E?style=flat-square&logo=aframe&logoColor=white"/> <img src="https://img.shields.io/badge/Open_ai-412991?style=flat-square&logo=openai&logoColor=white"/>

## 알고리즘
1. 유저에게서 post방식으로 사진과 prompt를 입력받거나 특징을 입력받고 받은 특징과 chat gpt api로 prompt를 생성.

2. 입력받은 파일을 확인하고 Pillow라이브러리를 통해 해상도 조정.

3. 조정된 사진은 static폴더에 저장되고 img_generating_clear_canvas.py에서 투명 캔버스를 포함한 더 큰 해상도의 사진으로 변환.

4. 변환된 사진은 chat gpt api를 이용하여 outpainting됨.

5. outpainting이 된 파일은 static폴더에 저장되고 해당 파일명을 return함.

6. return 받은 파일명으로 이미지 파일을 읽고, 스토리보드를 추가하여 영상화 할 것인지, 이미지로 VR환경을 만들 것 인지 물어봄.

7. 그냥 VR 환경을 만들면 이미지의 위,아래에 공간을 만들어 A-frame으로 VR환경을 만듬.

8. 영상화를 원하면 runway api로 영상을 만들고 A-frame으로 vr환경을 만들어 줌. 
