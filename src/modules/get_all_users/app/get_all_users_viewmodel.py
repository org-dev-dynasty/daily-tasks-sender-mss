from typing import List, Optional

from shared.domain.entities.user import User


class UserViewmodel:
  id: str
  name: str
  email: str
  phone: Optional[str]
  password: str
  
  def __init__(self, id: str, name: str, email: str, phone: Optional[str], password: str) -> None:
    self.id = id
    self.name = name
    self.email = email
    self.phone = phone
    self.password = password
    
  def to_dict(self) -> dict:
    return {
      "id": self.id,
      "name": self.name,
      "email": self.email,
      "phone": self.phone,
      "password": self.password
    }
    
    
class GetAllUsersViewmodel:
  def __init__(self, users: List[User]) -> None:
    self.users_viewmodel_list = [UserViewmodel(user.user_id, user.name, user.email, user.phone, user.password).to_dict() for user in users]
    
  def to_dict(self):
    return {
      "users": [viewmodel.to_dict() for viewmodel in self.users_viewmodel_list],
      "message": "All users have been retrieved successfully!"
    }
  
  