from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class ConfirmUserEmailUsecase:
  def __init__(self, repo: IUserRepository):
    self.repo = repo
  
  def __call__(self, email: str, verification_code: str) -> User:
    if not User.validate_email(email):
      raise EntityError('email')
    if len(verification_code) != 6:
      raise EntityError('verification_code')
    
    user = self.repo.confirm_user(email, verification_code)
    
    if user is None:
      raise NoItemsFound('email')
    
    return user
    
    