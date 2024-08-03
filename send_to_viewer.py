import requests

def upload_file(img):
    # 다른 서버로 전송할 URL
    other_server_url = 'https://port-0-flashback-viewer-lz26g1zp33dccd96.sel4.cloudtype.app'

    # 파일 리스트 구성
    files_to_send = []
    filename = 'uploaded_file'
    content_type = 'application/octet-stream'
    files_to_send.append(('files', (filename, img, content_type)))

    try:
        # 다른 서버로 파일 전송
        response = requests.post(other_server_url, files=files_to_send)
        response.raise_for_status()  # HTTP 에러가 있는지 확인
    except requests.exceptions.RequestException as e:
       raise Exception(f"파일 업로드 중 오류가 발생했습니다: {str(e)}")