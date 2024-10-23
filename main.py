from flask import Flask, render_template, request, session, redirect
from PIL import Image
import app
import img_generating_clear_canvas
import img_prompt
from random import randint
import illegal_pormpt
import img_to_mp4
import urllib.request
import make_music

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'svg', 'webp', 'ico']
flask = Flask(__name__)
flask.secret_key = 'LN$oaYB9-5KBT7G'
# 요청 객체 생성
REQUEST_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'audio/mpeg, audio/x-mpeg, audio/x-mpeg-3, audio/x-mpeg-4, audio/mp3, audio/aac, audio/aacp, audio/x-aac'
}

def allowed_file(filename: str) -> bool:
    '''이미지가 변환 가능한 확장자 명을 가졌는지 확인'''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@flask.route("/")
def main():
    return render_template("index.html")

@flask.route("/viewer")
def viewer():
    return render_template("viewer.html",file=session['file_name'])#+'_faded')

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
    """이미지를 같은 비율의 크기로 리사이즈 하는 함수(최대 512 X 512)"""
    width, height = img.size
    new_size = (512, int((height / width) * 512)) if width >= height else (int((width / height) * 512), 512)

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
        app.config["prompt"] = prompt    # 앱 설정에 프롬프트 저장 및 이미지 처리 호출
        app.image_processing(session['file_name'])
        imgs = img_generating_clear_canvas.second_canvas(session['file_name'])
        out = app.process_images_with_openai(imgs[0],imgs[1],prompt,1)
        for idx, data in enumerate(out):
            app.download_and_save_image(data['url'], f"static/{session['file_name']}_cropped.png")
            img2 = Image.open(f"static/{session['file_name']}_cropped.png").resize((1800,1800), Image.LANCZOS)
            img2.save(f"static/{session['file_name']}_cropped.png")
            print(f"{idx + 2}번째 이미지가 성공적으로 다운로드되었습니다.")
        try:
            music_url = make_music.generate_music(prompt)
            req = urllib.request.Request(music_url, headers=REQUEST_HEADER) # 요청 객체 생성
            with urllib.request.urlopen(req) as response:   # URL 열기
                content = response.read()   # 응답 내용 읽기
                with open(f'static/{session["file_name"]}.mp3', 'wb') as f:
                    f.write(content)
            print("mp3 파일 다운로드 완료.")
        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            print(f"URLError: {e.reason}")
        img_generating_clear_canvas.paste_imgs(session['file_name'])
        return session['file_name']  # 처리된 파일 이름 반환
    else:
        return "파일이 전송되지 않았거나 지원하지 않는 방식입니다.", 400
    
@flask.route("/post_video", methods=['POST'])
def post_video():
    Storyboard = request.form.get("storyboard","")
    file_name = session['file_name']
    try:
        video_url = img_to_mp4.video_generate(file_name,Storyboard)[0]
        req = urllib.request.Request(video_url, headers=REQUEST_HEADER) # 요청 객체 생성
        with urllib.request.urlopen(req) as response:   # URL 열기
            content = response.read()   # 응답 내용 읽기
            with open(f'static/{session["file_name"]}.mp4', 'wb') as f:
                f.write(content)
        print("RUNWAY API에서 영상 저장완료")
        return redirect("/viewer_video")
    except Exception as e:
        print(e)
        return 500

if __name__ == '__main__':  #C언어의 main 함수와 같은 개념의 조건문
    flask.run(debug=True,host='0.0.0.0')