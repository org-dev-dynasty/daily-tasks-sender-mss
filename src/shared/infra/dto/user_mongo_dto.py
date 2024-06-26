from typing import Optional

from src.shared.domain.entities.user import User


class UserMongoDTO:
  user_id: Optional[str]
  name: str
  email: str
  phone: Optional[str]
  password: str
  
  def __init__(self, user_id: Optional[str], name: str, email: str, phone: Optional[str], password: str):
    self.user_id = user_id
    self.name = name
    self.email = email
    self.phone = phone
    self.password = password
    
  def from_mongo(data) -> "UserMongoDTO":
    objId = data._id
    userId = str(objId)
    
    return UserMongoDTO(
      user_id=userId,
      name=data.name,
      email=data.email,
      phone=data.phone,
      password=data.password
    )
  
  def to_entity(dto: "UserMongoDTO") -> User:
    return User()