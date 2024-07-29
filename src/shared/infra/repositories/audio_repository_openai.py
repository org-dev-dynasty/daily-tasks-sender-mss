import openai
from src.shared.domain.irepositories.audio_repository_interface import IAudioRepository
from src.shared.environments import Environments

class AudioRepositoryOpenAI(IAudioRepository):
  def __init__(self):
    self.api_key = Environments.get_envs().open_ai_api_key
    openai.api_key = self.api_key

  def speech_to_text(self, audio_file) -> str:  
    print(f"name of file: {audio_file.name}")  
    try:
      response = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            language="pt"
        )
      return response['text']
    
    except Exception as e:
      print(f'ERROR TRANSCRIBING AUDIO: ')
      print(str(e))
      raise ValueError("An error occurred while transcribing audio")