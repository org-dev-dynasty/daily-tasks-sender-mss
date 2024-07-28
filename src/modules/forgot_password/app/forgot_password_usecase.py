from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class ForgotPasswordUsecase:
  def __init__(self, repo: IUserRepository):
    self.repo = repo
    
  def __call__(self, email: str):
    if not User.validate_email(email):
      raise EntityError("email")
    
    user = self.repo.get_user_by_email(email=email)
    
    if not user:
      raise NoItemsFound("user")
    
    self.repo.forgot_password(email=email)
    
    return