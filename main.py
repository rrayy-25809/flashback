from flask import Flask, render_template, request, redirect
from base64 import b64encode
from random import randint
from PIL import Image
import api
import io

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'svg', 'webp', 'ico'])   #변환 가능한 확장자명들
app = Flask(__name__) #서버 선언

def convert_and_send(resized_img,prompt, seed, position):
    # 리사이즈된 이미지를 다시 파일 객체로 변환
    img_byte_arr = io.BytesIO()
    resized_img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    # API 요청에 사용하기 위해 Base64로 변환
    return api.request_api(toB64(img_byte_arr),prompt, seed, position)  # API 요청 보내기

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
    if f and allowed_file(f.filename):  # 파일이 존재하고 변환 가능한 확장자 명을 가졌다면
        img = Image.open(io.BytesIO(f.read()))  # 이미지 파일을 읽고 Pillow로 열기
        width, height = img.size  # 이미지의 해상도 가져오기
        print(f"Original resolution: {width}x{height}")  # 원본 이미지 해상도를 출력

        if width>=height:
            new_width = 1024
            new_height = int((float(height)/float(width))*1024)
        else:
            new_height = 1024
            new_width = int((float(width)/float(height))*1024)

        # 이미지 크기 조정
        resized_img = img.resize((new_width, new_height),Image.LANCZOS)
        print(f"Resized resolution: {new_width}x{new_height}")  # 변경된 이미지 해상도 출력

        #리사이즈된 이미지를 자름
        crop_width = int(new_width/2)
        resized_img_1 = resized_img.crop((0,0,crop_width,new_height))
        resized_img_2 = resized_img.crop((crop_width,0,new_width,new_height))

        seed = randint(100000,999999) #랜덤 시드 값
        outpainted_img_1 = convert_and_send(resized_img_1,prompt, seed, 1024 - crop_width)
        outpainted_img_2 = convert_and_send(resized_img_2,prompt, seed, 0)

        if (outpainted_img_1!=None and outpainted_img_2!=None):
            image1 = Image.open(outpainted_img_1)
            image2 = Image.open(outpainted_img_2)

            new_image = Image.new('RGB',(2048, 1024), (250,250,250))
            new_image.paste(image1,(0,0))
            new_image.paste(image2,(1024,0))
            new_image.save("static/merged_image.jpg","JPEG")
        else:
            raise Exception(f"{f.filename} 파일에 예상하지 못한 오류가 존재합니다.")
        api.reset_count()
        return redirect("/viewer")
    else:
        raise Exception(f"{f.filename} 파일에 예상하지 못한 오류가 존재합니다.")

if __name__ == '__main__':  #C언어의 main 함수와 같은 개념의 조건문
    app.run(debug=True,host='0.0.0.0')
