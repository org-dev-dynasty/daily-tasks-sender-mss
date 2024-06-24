from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def create_user(self, name: str, email: str, phone: str, password: str) -> User:
        pass

    @abstractmethod
    def login(self, email, password):
        pass

    # @abstractmethod
    # def get_user_by_id(self, user_id: int) -> User:
    #   pass
