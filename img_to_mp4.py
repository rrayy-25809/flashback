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
  # Point this at your own image file
  prompt_image='https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg',
  prompt_text='string',
)
task_id = task.id

# Poll the task until it's complete
time.sleep(10)  # Wait for a second before polling
task = client.tasks.retrieve(task_id)
while task.status not in ['SUCCEEDED', 'FAILED']:
  time.sleep(10)  # Wait for ten seconds before polling
  task = client.tasks.retrieve(task_id)

print('Task complete:', task)