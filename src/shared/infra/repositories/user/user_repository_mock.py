from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository


class UserRepositoryMock(IUserRepository):
    def __init__(self):
        self.users = [
            User("Digao", "digao@gmail.com", "11999999999", "Teste12@"),
            User("Ale", "ale@gmail.com", "11299999999", "Teste1@"),
            User("Lucao", "lucao@gmail.com", "11399999999", "Teste13@"),
            User("Brenheta", "brenheta@gmail.com", "11499999999", "Teste14@"),
            User("Merola", "merola.gay@gmail.com", "11599999999", "Teste15@"),
        ]

    def get_all_users(self) -> List[User]:
        users = self.users
        return users

    def create_user(self, name: str, email: str, phone: str, password: str) -> User:
        user = User(name, email, phone, password)
        self.users.append(user)
        return user

    def get_user_by_id(self, user_id: int) -> User:
        user = next((user for user in self.users if user.user_id == user_id), None)
        return user

    def login(self, email, password) -> bool:
        if self.users is not None:
            for user in self.users:
                if user.email == email:
                    if user.password == password:
                        print("Usuário Logado!")
                        return True
                    print("Senha incorreta")
                    return False
                print("E-mail não encontrado")
                return False
        else:
            return False