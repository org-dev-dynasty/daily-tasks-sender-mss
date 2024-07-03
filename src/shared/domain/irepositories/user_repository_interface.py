from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.user import User


class IUserRepository(ABC):
  @abstractmethod
  def get_all_users(self) -> List[User]:
    pass
  
  @abstractmethod
  def create_user(self, user: User) -> User:
    pass

  def login_user(self, login: str, password: str) -> dict:
    pass
  
  def get_user_by_email(self, email: str) -> User:
    pass
  
  # @abstractmethod
  # def get_user_by_id(self, user_id: int) -> User:
  #   pass