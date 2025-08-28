# RE:mind 🎗️ - FLASHBACK
**생성형 AI 기반 사진 확장(Outpainting) + VR 기술을 융합한 우울증 치료·예방 프로그램**

---

## 📌 프로젝트 개요
우울증은 전 세계적으로 3억 명 이상이 겪고 있으며, 기존의 약물치료·상담치료는 부작용, 장기간 치료, 비용 문제 등으로 접근성이 낮습니다.  
본 프로젝트는 **긍정적 기억의 회상 효과**를 기반으로, **AI와 VR을 활용하여 우울증 치료와 예방을 지원하는 새로운 접근 방식**을 제안합니다.

- 📷 **AI Outpainting** : 사용자가 업로드한 사진을 AI가 확장하여 더 넓은 장면을 생성  
- 🕶️ **VR 체험** : 확장된 이미지를 A-Frame VR 환경에서 경험
- 🎵 **AI 음악 생성 (Suno)** : 감정 맞춤 음악을 생성해 치료적 몰입 강화  
- 🎬 **AI 영상 생성 (Runway)** : 확장된 이미지와 음악을 결합해 짧은 영상 제작 가능  
- 🎯 **목표** : 정서 환기, 긍정적 경험 강화, 우울증 예방 및 치료 보조

---

## 🛠️ Tech Stack

### 🖥️ Languages
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

### ⚙️ Frameworks & Libraries
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![A-Frame](https://img.shields.io/badge/Aframe.js-EF2D5E?style=for-the-badge&logo=mozilla&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)

---

## ⚡ 작동 알고리즘 (Workflow)

1. **이미지 업로드**
   - 사용자가 웹에서 사진과 프롬프트(선택)를 업로드
   - 프롬프트가 없을 경우 OpenAI API로 이미지 특징을 분석하여 자동 생성

2. **이미지 전처리**
   - Pillow로 원본 사진 크기 조정
   - 해상도 손실을 최소화하기 위해 이미지를 분할

3. **Outpainting**
   - Segmind를 이용해 분할된 이미지를 확장
   - 확장된 이미지를 이어붙여 고해상도 이미지 완성

4. **VR 변환**
   - Flask 서버에서 결과 이미지를 A-Frame.js로 전달
   - 웹 브라우저 상에서 360° VR처럼 경험 가능

5. **멀티모달 확장**
   - **Suno** : 사용자의 감정/사진 분위기에 맞는 음악 자동 생성
   - **Runway** : 확장된 이미지와 음악을 합쳐 몰입형 동영상 생성

---

## 📌 향후 개선 계획
- 📱 모바일 앱 전환 (웹→앱 변환 시스템 활용)  
- 🔧 Outpainting 결과물 자연스러움 개선 (세분화 Inpainting 알고리즘 적용)  

---

## 📚 관련 논문  
  - *The Effects of Positive Autobiographical Memory Recall in Repairing Sad Mood for Depressed Individuals*  
  - *The Role of Positive Emotion and Contributions of Positive Psychology in Depression Treatment*  

---
