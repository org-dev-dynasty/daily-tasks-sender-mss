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