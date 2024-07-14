from flask import Flask, render_template, request, redirect
from base64 import b64encode
from PIL import Image
import io
import app as apppppp
import img_generating_clear_canvas

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'svg', 'webp', 'ico'])   #변환 가능한 확장자명들
app = Flask(__name__) #서버 선언

def convert_and_send(resized_img, prompt, seed, position):
    # 리사이즈된 이미지를 다시 파일 객체로 변환
    img_byte_arr = io.BytesIO()
    resized_img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    # API 요청에 사용하기 위해 Base64로 변환
    #return api.request_api(toB64(img_byte_arr),prompt, seed, position)  # API 요청 보내기

def toB64(img_file:str):
    '''이미지를 API가 알아들을 수 있게 변환'''
    return str(b64encode(img_file.read()))[2:-1]

def allowed_file(filename:str):
    '''이미지가 변환 가능한 확장자 명을 가졌는지 확인'''
    if '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return  True
    return False

@app.route("/")
def main():
    return render_template("index.html")#메인페이지

@app.route("/viewer")
def viewer():
    return render_template("viewer.html")

@app.route("/post_image", methods=['POST'])
def post_image():
    if request.method != 'POST' : return redirect('/')  #파일이 제대로 입력받지 못했다면 메인페이지로 이동
    f = request.files['file']
    prompt = request.form['prompt']
    """if prompt==None:
        prompt = generate_prompt()"""
    if f and allowed_file(f.filename):  # 파일이 존재하고 변환 가능한 확장자 명을 가졌다면
        img = Image.open(io.BytesIO(f.read()))  # 이미지 파일을 읽고 Pillow로 열기
        img.save("static/original_image.png","PNG")
        img_generating_clear_canvas.canvas_clear() #이미지에 투명 캔버스 씌우는 코드
        print("wddf")
        apppppp.image_processing()  #변환된 이미지를 outpainting하는 코드
        # if width>=height:
        #     new_width = 1024
        #     new_height = int((float(height)/float(width))*1024)
        # else:
        #     new_height = 1024
        #     new_width = int((float(width)/float(height))*1024)

        # # 이미지 크기 조정
        # resized_img = img.resize((new_width, new_height),Image.LANCZOS)
        # print(f"Resized resolution: {new_width}x{new_height}")  # 변경된 이미지 해상도 출력

        #TODO: 새로운 API 이용해서 resized_img와 prompt 변수 입력받아서 아웃페인팅

        return redirect("/viewer")
    else:
        raise Exception(f"{f.filename} 파일에 예상하지 못한 오류가 존재합니다.")

if __name__ == '__main__':  #C언어의 main 함수와 같은 개념의 조건문
    app.run(debug=True,host='0.0.0.0')
