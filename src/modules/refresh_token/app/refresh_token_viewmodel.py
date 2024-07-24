class RefreshTokenViewmodel:
  access_token: str
  id_token: str
  refresh_token: str
  
  def __init__(self, access_token: str, id_token: str, refresh_token: str):
    self.access_token = access_token
    self.id_token = id_token
    self.refresh_token = refresh_token
    
  def to_dict(self):
    return {
      'access_token': self.access_token,
      'id_token': self.id_token,
      'refresh_token': self.refresh_token,
      'message': 'Tokens refreshed successfully'
    }