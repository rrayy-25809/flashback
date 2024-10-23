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
import fade_in_out

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'svg', 'webp', 'ico']
flask = Flask(__name__)
flask.secret_key = 'LN$oaYB9-5KBT7G'

# 사용자 에이전트 및 오디오 요청 헤더 설정
REQUEST_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'audio/mpeg, audio/x-mpeg, audio/x-mpeg-3, audio/x-mpeg-4, audio/mp3, audio/aac, audio/aacp, audio/x-aac'
}

def allowed_file(filename: str) -> bool:
    '''이미지가 변환 가능한 확장자 명을 가졌는지 확인'''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_resize(img: Image) -> Image:
    '''이미지를 같은 비율로 최대 512x512 크기로 리사이즈'''
    width, height = img.size
    new_size = (512, int((height / width) * 512)) if width >= height else (int((width / height) * 512), 512)
    resized_img = img.resize(new_size, Image.LANCZOS)
    print(f"Resized resolution: {new_size[0]}x{new_size[1]}")
    return resized_img

def download_and_save_file(url: str, file_path: str, file_type: str):
    '''파일을 URL에서 다운로드하여 저장'''
    try:
        req = urllib.request.Request(url, headers=REQUEST_HEADER)
        with urllib.request.urlopen(req) as response:
            content = response.read()
            with open(file_path, 'wb') as f:
                f.write(content)
        print(f"{file_type} 파일 다운로드 완료: {file_path}")
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")

def process_image_upload(file, description, is_remix):
    '''이미지 업로드 처리 및 이미지 가공 작업 수행'''
    if not allowed_file(file.filename):
        return "파일이 지원하지 않는 형식입니다.", 400
    
    if illegal_pormpt.illegal_prompt1(description):
        return "프롬프트 에러", 400

    prompt = description if is_remix else img_prompt.ask_openai(description)
    session['file_name'] = str(randint(1, 999))  # 랜덤 파일 이름 생성

    img = image_resize(Image.open(file.stream))
    img.save("static/original_image.png", "PNG")

    img_generating_clear_canvas.canvas_clear()
    app.config["prompt"] = prompt
    app.image_processing(session['file_name'])
    
    imgs = img_generating_clear_canvas.second_canvas(session['file_name'])
    out = app.process_images_with_openai(imgs[0], imgs[1], prompt, 1)
    
    for idx, data in enumerate(out):
        download_and_save_file(data['url'], f"static/{session['file_name']}_cropped.png", "이미지")
        img2 = Image.open(f"static/{session['file_name']}_cropped.png").resize((1800, 1800), Image.LANCZOS)
        img2.save(f"static/{session['file_name']}_cropped.png")
        print(f"{idx + 2}번째 이미지가 성공적으로 다운로드되었습니다.")

    music_url = make_music.generate_music(prompt)
    download_and_save_file(music_url, f'static/{session["file_name"]}.mp3', "음악")
    img_generating_clear_canvas.paste_imgs(session['file_name'])
    return session['file_name']

@flask.route("/")
def main():
    return render_template("index.html")

@flask.route("/viewer")
def viewer():
    file = session['file_name']
    return render_template("viewer.html", file=file, color=fade_in_out.find_color(file))

@flask.route("/viewer_video")
def viewer_video():
    file = session['file_name']
    return render_template("viewer_video.html", file=file, color=fade_in_out.find_color(file))

@flask.route("/information")
def info():
    return render_template("info.html")

@flask.route("/input")
def input_page():
    return render_template("input.html")

@flask.route("/post_image", methods=['POST'])
def post_image():
    '''이미지 업로드 후 처리 및 프롬프트 기반 이미지 생성'''
    f = request.files.get('image')
    description = request.form.get('prompt', '')
    is_remix = "true" == request.form.get('is_remix')
    
    if f:
        return process_image_upload(f, description, is_remix)
    return "파일이 전송되지 않았습니다.", 400

@flask.route("/post_video", methods=['POST'])
def post_video():
    '''영상 생성 요청 및 파일 다운로드 처리'''
    Storyboard = request.form.get("storyboard", "")
    file_name = session['file_name']
    try:
        video_url = img_to_mp4.video_generate(file_name, Storyboard)[0]
        download_and_save_file(video_url, f'static/{session["file_name"]}.mp4', "비디오")
        return "파일이 잘 전송된!",200
    except Exception as e:
        print(e)
        return "파일이 잘 전송되지 않은!",500

if __name__ == '__main__':
    flask.run(debug=True, host='0.0.0.0')