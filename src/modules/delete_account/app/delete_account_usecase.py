from src.shared.domain.irepositories.user_repository_interface import IUserRepository


class DeleteAccountUsecase:
  def __init__(self, repo: IUserRepository):
    self.repo = repo
    
  def __call__(self, user_id):
    self.repo.delete_account(user_id)
    
    return 'User deleted'