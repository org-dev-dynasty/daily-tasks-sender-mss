from shared.domain.irepositories.user_repository_interface import IUserRepository
from shared.helpers.errors.usecase_errors import NoItemsFound


class GetAllUsersUsecase:
  def __init__(self, repo: IUserRepository):
    self.repo = repo
    
  def execute(self):
    users = self.repo.get_all_users()
    
    if len(users) == 0:
      raise NoItemsFound("users")
    
    return users