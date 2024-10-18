from flask import Flask, render_template, request, session
from PIL import Image
import app
import img_generating_clear_canvas
import img_prompt
from random import randint
import illegal_pormpt
import img_to_mp4
import urllib.request

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'svg', 'webp', 'ico'}
flask = Flask(__name__)
flask.secret_key = 'LN$oaYB9-5KBT7G'

def allowed_file(filename: str) -> bool:
    '''이미지가 변환 가능한 확장자 명을 가졌는지 확인'''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@flask.route("/")
def main():
    return render_template("index.html")#메인페이지

@flask.route("/viewer")
def viewer():
    return render_template("viewer.html",file=session['file_name']+'_faded')

@flask.route("/viewer_video")
def viewer_video():
    return render_template("viewer_video.html",file=session['file_name'])

@flask.route("/information")
def info():
    return render_template("info.html")

@flask.route("/input")
def input_page():
    return render_template("input.html")

def image_resize(img: Image) -> Image:
    """이미지를 같은 비율의 크기로 리사이즈 하는 함수(최대 1024 X 1024)"""
    width, height = img.size
    new_size = (1024, int((height / width) * 1024)) if width >= height else (int((width / height) * 1024), 1024)

    resized_img = img.resize(new_size, Image.LANCZOS)
    print(f"Resized resolution: {new_size[0]}x{new_size[1]}")
    return resized_img

@flask.route("/post_image", methods=['POST'])
def post_image():
    f = request.files.get('image')
    description = request.form.get('prompt', '')
    is_remix = "true"==request.form.get('is_remix')

    # 파일 존재 및 지원 형식 확인
    if f and allowed_file(f.filename):
        if illegal_pormpt.illegal_prompt1(description):
            return "프롬포트 에러", 400
        if is_remix:
            prompt = description
        else:
            prompt = img_prompt.ask_openai(description)  # OpenAI에서 프롬프트 생성
        session['file_name'] = str(randint(1, 999))  # 랜덤 파일 이름 생성
        
        # 이미지 처리
        img = image_resize(Image.open(f.stream))
        img.save("static/original_image.png", "PNG")
        img_generating_clear_canvas.canvas_clear()  # 캔버스 클리어
        
        # 앱 설정에 프롬프트 저장 및 이미지 처리 호출
        app.config["prompt"] = prompt
        app.image_processing(session['file_name'])
        img_generating_clear_canvas.after_process_image(session['file_name'])

        return session['file_name']  # 처리된 파일 이름 반환
    else:
        return "파일이 전송되지 않았거나 지원하지 않는 방식입니다.", 400
    
@flask.route("/post_video", methods=['POST'])
def post_video():
    Storyboard = request.form.get("storyboard","")
    file_name = session['file_name']
    video_url = img_to_mp4.video_generate(file_name,Storyboard)
    urllib.request.urlretrieve(video_url,f"static/{file_name}.mp4")
    print("RUNWAY API에서 영상 저장완료")
    return file_name

if __name__ == '__main__':  #C언어의 main 함수와 같은 개념의 조건문
    flask.run(debug=True,host='0.0.0.0')