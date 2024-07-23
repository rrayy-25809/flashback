import zipfile
from io import BytesIO

def create_vr_html():
    # 360 VR 이미지를 보여주는 HTML 콘텐츠를 생성하는 함수입니다.
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>360 VR Image</title>
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                overflow: hidden;
            }}
            #vr {{
                width: 100%;
                height: 100%;
            }}
        </style>
    </head>
    <body>
        <div id="vr"></div>
        <script src="https://aframe.io/releases/1.2.0/aframe.min.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function () {{
                var scene = document.createElement('a-scene');
                var sky = document.createElement('a-sky');
                sky.setAttribute('src', 'img.png');
                scene.appendChild(sky);
                document.getElementById('vr').appendChild(scene);
            }});
        </script>
    </body>
    </html>
    """
    return html_content

def create_zip():
    # 메모리 버퍼를 사용하여 zip 파일을 생성합니다.
    file_folder = BytesIO()
    
    # 이미지를 바이너리 모드로 엽니다.
    with open("static/outputimage.png", 'rb') as img:
        # HTML 콘텐츠를 생성합니다.
        html = create_vr_html()
        
        # zip 파일을 쓰기 모드로 엽니다.
        with zipfile.ZipFile(file_folder, 'w') as zip_folder:
            try:
                # zip 파일에 이미지를 추가합니다.
                zip_folder.writestr("img.png", img.read())
                # zip 파일에 HTML 파일을 추가합니다.
                zip_folder.writestr("index.html", html)
            except Exception as error:
                # 오류가 발생하면 오류를 출력합니다.
                print(error)
    
    # 메모리 버퍼의 포인터를 시작 위치로 되돌립니다.
    file_folder.seek(0)
    return file_folder
