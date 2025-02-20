from abc import ABC, abstractmethod

class IAudioRepository(ABC):
  @abstractmethod
  def speech_to_text(self, audio_path) -> str:
    pass