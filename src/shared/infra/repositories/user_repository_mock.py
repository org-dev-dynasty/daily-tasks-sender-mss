from typing import List, Tuple
from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem


class UserRepositoryMock(IUserRepository):
    def __init__(self):
        self.users = [
            User("Digao", "digao@gmail.com", "11999999999", "Teste12@", True, False),
            User("Ale", "ale@gmail.com", "11299999999", "Teste1@", True, False),
            User("Lucao", "lucao@gmail.com", "11399999999", "Teste13@", False, False),
            User("Brenheta", "brenheta@gmail.com", "11499999999", "Teste14@", True, False),
            User("Merola", "merola.gay@gmail.com", "11599999999", "Teste15@", True, True, '1'),
        ]

    def create_user(self, user: User) -> User:
        self.users.append(user)
        return user

    def login(self, email: str, password: str) -> User:
        user = next((user for user in self.users if user.email == email and user.password == password), None)
        return user

    def get_user_by_id(self, user_id: int) -> User:
        user = next((user for user in self.users if user.user_id == user_id), None)
        return user

    def get_user_by_email(self, email: str) -> User:
        user = next((user for user in self.users if user.email == email), None)
        return user
    
    def confirm_user(self, email: str, verification_code: str) -> User:
        user = next((user for user in self.users if user.email == email), None)
        return user
    
    def create_user_oauth(self, user) -> dict:
        if self.get_user_by_email(user.email):
            raise DuplicatedItem("email")
        user.user_id = str(len(self.users) + 1)
        self.users.append(user)
        return {"message": "User created successfully"}
    
    def refresh_token(self, refresh_token: str) -> Tuple[str, str]:
        return ("access_token here", "refresh_token here")