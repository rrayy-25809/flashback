import os
import time
import dotenv
from runwayml import RunwayML

# .env 파일에서 환경 변수 불러오기
dotenv.load_dotenv()

# API 키 불러오기
client = RunwayML(api_key=os.getenv('RUNWAY_API_SECRET'))

# 이미지에서 비디오 생성 작업
task = client.image_to_video.create(
  model='gen3a_turbo',
  #이미지 파일 받기 (https:// 로 시작해야함)
  prompt_image='https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg',
  prompt_text='string',
)
task_id = task.id

# Poll the task until it's complete
time.sleep(10) #10초간격으로 서버에 작업 상태를 확인함
task = client.tasks.retrieve(task_id)
while task.status not in ['SUCCEEDED', 'FAILED']:
  time.sleep(10)
  task = client.tasks.retrieve(task_id)

print('Task complete:', task)