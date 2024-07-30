import openai
import os
from src.shared.domain.irepositories.audio_repository_interface import IAudioRepository
from src.shared.environments import Environments
import requests

class AudioRepositoryOpenAI(IAudioRepository):
  def __init__(self):
    self.api_key = Environments.get_envs().open_ai_api_key
    openai.api_key = self.api_key

  def speech_to_text(self, file) -> str:
    try:      
      # audio_file = open(path, "rb")

      file_bytes, filename = file
      
      just_filename = filename.split('.')[0]

      
      mime = f"audio/{filename.split('.')[-1]}"
      
      request_files = {
        "file": (just_filename, file_bytes, mime)
      }
      data = {
        "model": "whisper-1"
      }      
      
      response = requests.post('https://api.openai.com/v1/audio/transcriptions', files=request_files, headers={
        'Authorization': f'Bearer {Environments.get_envs().open_ai_api_key}'
      }, data=data)
      
      print(response.status_code)
      
      print('response.json(): ')
      print(response.json())
      
      # delete the file
      # os.remove(path)
      
      return response['text']
    
    except Exception as e:
      print(f'ERROR TRANSCRIBING AUDIO: ')
      print(str(e))
      raise ValueError("An error occurred while transcribing audio")