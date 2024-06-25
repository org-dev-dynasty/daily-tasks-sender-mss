from typing import Optional

from src.shared.infra.repositories.database.models import UserModel
from src.shared.domain.entities.user import User


class UserPostgresDTO:
  user_id: Optional[str]
  name: str
  email: str
  phone: Optional[str]
  password: str
  
  def __init__(self, user_id: Optional[str], name: str, email: str, phone: Optional[str], password: str) -> None:
    self.user_id = user_id
    self.name = name
    self.email = email
    self.phone = phone
    self.password = password
    
  @staticmethod
  def from_postgres(model: UserModel) -> User:
    print(f'from postgres: email={model.email}, password={model.password}, user_id={model.user_id}')
    return UserPostgresDTO(
      model.user_id,
      model.name,
      model.email,
      model.phone,
      model.password
    )
  
  @staticmethod
  def to_entity(self) -> User:
    return User(
      user_id=self.user_id,
      name=self.name,
      email=self.email,
      phone=self.phone,
      password=self.password
    )