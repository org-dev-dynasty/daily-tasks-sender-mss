import openai
from src.shared.domain.irepositories.audio_repository_interface import IAudioRepository
from src.shared.environments import Environments

class AudioRepositoryOpenAI(IAudioRepository):
  def __init__(self):
    self.api_key = Environments.get_envs().open_ai_api_key
    openai.api_key = self.api_key

  def speech_to_text(self, audio_file) -> str:
    try:
      name, buffer = audio_file
      response = openai.Audio.transcribe(
            model="whisper-1",
            file=(name, buffer),
            language="pt"
        )
      return response['text']
    
    except Exception as e:
      print(f'ERROR TRANSCRIBING AUDIO: ')
      print(str(e))
      raise ValueError("An error occurred while transcribing audio")