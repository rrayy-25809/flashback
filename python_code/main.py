from flask import Flask, render_template, request, redirect
from base64 import b64encode
from PIL import Image
import io
import app
import img_generating_clear_canvas
import img_prompt

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'svg', 'webp', 'ico'])   #변환 가능한 확장자명들
flask = Flask(__name__) #서버 선언

def allowed_file(filename:str):
    '''이미지가 변환 가능한 확장자 명을 가졌는지 확인'''
    if '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return  True
    return False

@flask.route("/")
def main():
    return render_template("index.html")#메인페이지

@flask.route("/viewer")
def viewer():
    return render_template("viewer.html")

@flask.route("/start/<string:page>") #후에 추가될 화면의 함수
def start(page):
    """하지만 Flask에서 내부링크를 연결하기 위한 사용법
    <a hre="{{url_for('index')}}"> 이동 </a>"""
    if page=="extend":
        return render_template("IDKsd.html")
    elif page=="remix":
        return render_template("IDK.html")
    else:
        return render_template("IDK.html")

@flask.route("/post_image", methods=['POST'])
def post_image():
    if request.method != 'POST' : return redirect('/')  #파일이 제대로 입력받지 못했다면 메인페이지로 이동
    f = request.files['file']
    prompt = request.form['prompt']
    """if prompt==None:
        prompt = generate_prompt()"""
    if f and allowed_file(f.filename):  # 파일이 존재하고 변환 가능한 확장자 명을 가졌다면
        img = image_resize(Image.open(io.BytesIO(f.read())))  # 이미지 파일을 읽고 Pillow로 열기
        img.save("static/original_image.png","PNG")
        img_generating_clear_canvas.canvas_clear() #이미지에 투명 캔버스 씌우는 코드
        # print("wddf") 
        app.image_processing()  #변환된 이미지를 outpainting하는 코드

        return redirect("/viewer")
    else:
        raise Exception(f"{f.filename} 파일에 예상하지 못한 오류가 존재합니다.")

def image_resize(img:Image):
    width,height = img.size
    if width>=height:
        new_width = 2048
        new_height = int((float(height)/float(width))*2048)
    else:
        new_height = 2048
        new_width = int((float(width)/float(height))*2048)

    # 이미지 크기 조정
    resized_img = img.resize((new_width, new_height),Image.LANCZOS)
    print(f"Resized resolution: {new_width}x{new_height}")  # 변경된 이미지 해상도 출력
    return resized_img

if __name__ == '__main__':  #C언어의 main 함수와 같은 개념의 조건문
    flask.run(debug=True,host='0.0.0.0')
