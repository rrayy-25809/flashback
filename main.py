from flask import Flask, render_template, request, redirect
from PIL import Image
import io
import app
import img_generating_clear_canvas
import img_prompt
from random import randint

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'svg', 'webp', 'ico'}
flask = Flask(__name__)
flask.secret_key = 'LN$oaYB9-5KBT7G'

file_name = ""

def allowed_file(filename: str) -> bool:
    '''이미지가 변환 가능한 확장자 명을 가졌는지 확인'''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@flask.route("/")
def main():
    return render_template("index.html")#메인페이지

@flask.route("/viewer")
def viewer():
    return render_template("viewer.html",file=file_name)

@flask.route("/information")
def info():
    return render_template("info.html")

@flask.route("/input")
def input_page():
    return render_template("input.html")

@flask.route("/post_image", methods=['POST'])
def post_image():
    if request.method != 'POST':
        return redirect('/')  #Invalid request, redirect to main page
    
    f = request.files.get('image')
    description = request.form.get('prompt', '')

    if f and allowed_file(f.filename):
        prompt = img_prompt.ask_openai(description)
        process_image(f.read(), prompt)
    else:
        return "Unsupported file format or no file uploaded.", 400

    return file_name

def image_resize(img: Image) -> Image:
    """Resize the image to a maximum of 2048x2048 while maintaining aspect ratio."""
    width, height = img.size
    new_size = (2048, int((height / width) * 2048)) if width >= height else (int((width / height) * 2048), 2048)

    resized_img = img.resize(new_size, Image.LANCZOS)
    print(f"Resized resolution: {new_size[0]}x{new_size[1]}")
    return resized_img

def process_image(f: bytes, prompt: str):
    global file_name
    file_name = str(randint(1, 999))

    img = image_resize(Image.open(io.BytesIO(f)))
    img.save("static/original_image.png", "PNG")
    img_generating_clear_canvas.canvas_clear()

    app.config["prompt"] = prompt
    app.image_processing(file_name)
    img_generating_clear_canvas.after_process_image(file_name)

if __name__ == '__main__':  #C언어의 main 함수와 같은 개념의 조건문
    flask.run(debug=True,host='0.0.0.0')