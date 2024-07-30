import openai
import os
from src.shared.domain.irepositories.audio_repository_interface import IAudioRepository
from src.shared.environments import Environments
import requests

class AudioRepositoryOpenAI(IAudioRepository):
  def __init__(self):
    self.api_key = Environments.get_envs().open_ai_api_key
    openai.api_key = self.api_key

  def speech_to_text(self, path) -> str:
    try:      
      audio_file = open(path, "rb")

      request_files = {
        "file": audio_file,
        "model": (None, "whisper-1"),
      }
      
      
      
      response = requests.post('https://api.openai.com/v1/audio/transcriptions', files=request_files, headers={
        'Content-Type': 'multipart/form-data',
        'Authorization': f'Bearer {Environments.get_envs().open_ai_api_key}'
      })
      
      print('response.json(): ')
      print(response.json())
      
      # delete the file
      os.remove(path)
      
      return response['text']
    
    except Exception as e:
      print(f'ERROR TRANSCRIBING AUDIO: ')
      print(str(e))
      raise ValueError("An error occurred while transcribing audio")