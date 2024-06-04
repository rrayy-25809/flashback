from flask import Flask, render_template, request, redirect
from base64 import b64encode
import api

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'svg', 'webp', 'ico'])   #변환 가능한 확장자명들
app = Flask(__name__) #서버 선언

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

@app.route("/post_image", methods=['POST'])
def post_image():
    if request.method != 'POST' : return redirect('/')  #파일이 제대로 입력받지 못했다면 메인페이지로 이동
    f = request.files['file']
    if f and allowed_file(f.filename):  #파일이 존재하고 변환 가능한 확장자 명을 가졌다면
        api.request_api(toB64(f))   #api 요청 보내기
        return redirect('/')
    else:
        raise Exception(f"{f.filename} 파일에 예상하지 못한 오류가 존재합니다.")

if __name__ == '__main__':  #C언어의 main 함수와 같은 개념의 조건문
    app.run(debug=True)
