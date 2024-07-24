class UserAPIGatewayDTO:
  user_id: str
  
  def __init__(self, user_id: str) -> None:
    self.user_id = user_id
    
  @staticmethod
  def from_api_gateway(data: dict) -> "UserAPIGatewayDTO":
    return UserAPIGatewayDTO(
      user_id=data['user_id']
    )
    
  def to_dict(self) -> dict:
    return {
      'user_id': self.user_id
    }