from src.shared.domain.irepositories.audio_repository_interface import IAudioRepository


class TranscribeAudioUsecase:
  def __init__(self, repo: IAudioRepository):
    self.repo = repo
    
  def __call__(self, audio_buffer, file_name):
    audio_transcribed = self.repo.speech_to_text(audio_buffer, file_name)
    
    return audio_transcribed
    