from shared.domain.irepositories.user_repository_interface import IUserRepository


class UserRepositoryCognito(IUserRepository):
  def get_all_users(self):
    return []