import os
import time
import dotenv
from runwayml import RunwayML

# .env 파일에서 환경 변수 불러오기
dotenv.load_dotenv()

# API 키 불러오기
client = RunwayML(api_key=os.getenv('RUNWAY_API_SECRET'))

def video_generate(file:str, story:str):
  # 이미지에서 비디오 생성 작업
  task = client.image_to_video.create(
    model='gen3a_turbo',
    prompt_image=f'https://playflashback.xyz/static/{file}.png',
    prompt_text=story,
  )
  task_id = task.id

  time.sleep(10)  #폴링 하기 전에 1초 기다리기
  task = client.tasks.retrieve(task_id)
  while task.status not in ['SUCCEEDED', 'FAILED']:
    time.sleep(10)  #폴링 하기 전에 1초 기다리기
    task = client.tasks.retrieve(task_id)

  print('Task complete:', task)
  return task.output