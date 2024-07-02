from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository


class UserRepositoryMock(IUserRepository):
    def __init__(self):
        self.users = [
            User("Digao", "digao@gmail.com", "11999999999", "Teste12@", True, False),
            User("Ale", "ale@gmail.com", "11299999999", "Teste1@", True, False),
            User("Lucao", "lucao@gmail.com", "11399999999", "Teste13@", False, False),
            User("Brenheta", "brenheta@gmail.com", "11499999999", "Teste14@", True, False),
            User("Merola", "merola.gay@gmail.com", "11599999999", "Teste15@", True, True, '1'),
        ]

    def get_all_users(self) -> List[User]:
        users = self.users
        return users

    def create_user(self, user: User) -> User:
        self.users.append(user)
        return user

    def login(self, email: str, password: str) -> User:
        user = next((user for user in self.users if user.email == email and user.password == password), None)
        return user

    def get_user_by_id(self, user_id: int) -> User:
        user = next((user for user in self.users if user.user_id == user_id), None)
        return user
