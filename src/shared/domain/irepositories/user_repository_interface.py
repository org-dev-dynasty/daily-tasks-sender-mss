from abc import ABC, abstractmethod
from typing import List, Tuple

from src.shared.domain.entities.user import User


class IUserRepository(ABC):  
  @abstractmethod
  def create_user(self, user: User) -> dict:
    pass

  @abstractmethod
  def login(self, login: str, password: str) -> dict:
    pass
  
  @abstractmethod
  def get_user_by_email(self, email: str) -> User:
    pass
  
  @abstractmethod
  def confirm_user(self, email: str, verification_code: str) -> User:
    pass
  
  @abstractmethod
  def create_user_oauth(self, user) -> dict:
    pass 
  
  @abstractmethod
  def refresh_token(self, refresh_token: str) -> Tuple[str, str]:
    pass
  
  @abstractmethod
  def get_all_users(self) -> List[User]:
    pass
  
  @abstractmethod
  def change_password(self, oldPassword: str, newPassword: str, access_token: str) -> dict:
    pass

  @abstractmethod
  def forgot_password(self, email: str) -> dict:
    pass
  
  @abstractmethod
  def delete_account(self, user_id: str) -> dict:
    pass  
  # @abstractmethod
  # def get_user_by_id(self, user_id: int) -> User:
  #   pass