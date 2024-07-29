class TranscribeAudioViewmodel:
  audio_transcribed: str
  
  def __init__(self, data_transcribed: str):
    self.audio_transcribed = data_transcribed
    
  def to_dict(self):
    return {
      'audio_transcribed': self.audio_transcribed
    }