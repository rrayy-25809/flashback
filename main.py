from flask import Flask, render_template, request, redirect
from base64 import b64encode
import api

def toB64(img_file):
    return str(b64encode(img_file.read()))[2:-1]

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)

def allowed_file(filename:str):
    if '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return  True
    else:
        return False
        

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/post_image", methods=['POST'])
def post_image():
    if request.method != 'POST' : return redirect('/')
    f = request.files['file']
    if f and allowed_file(f.filename):
        api.request_api(toB64(f))
        return redirect('/')
    else:
        raise Exception(f"{f.filename} 파일에 예상하지 못한 오류가 존재합니다.")

if __name__ == '__main__':
    app.run(debug=True)
