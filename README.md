# RE:mind 🎗️ - FLASHBACK

## 알고리즘
1. 유저에게서 파일과 프롬포트 입력받기(추후 개선될 예정)
2. 파일을 확인하고 Pillow라이브러리를 통해 크기 조정
3. 파일의 중앙을 기준으로 2등분, 기준이 될 위치 변수로 저장
4. 2등분 된 두 파일을 각각 같은 시드를 가지고 segmind API로 아웃페인팅
5. 아웃페인팅된 두 이미지를 저장된 변수를 기준으로 두 이미지를 병합
6. A-Frame 프레임워크로 가상환경을 만들고 병합된 이미지를 사용하여 VR처럼 볼 수 있게 표현
