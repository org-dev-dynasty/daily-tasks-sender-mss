from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class ConfirmUserEmailUsecase:
  def __init__(self, repo: IUserRepository):
    self.repo = repo
  
  def __call__(self, email: str, verification_code: str) -> User:
    print(f'chegou no usecase {email} {verification_code}')
    print(f'email: {email}')
    print(f'verification_code: {verification_code}')
    print(f'len verification_code: {len(verification_code)}')
    if not User.validate_email(email):
      raise EntityError('email')
    
    print(f'passou dos ifs')
    
    user = self.repo.confirm_user(email, verification_code)
    
    if user is None:
      raise NoItemsFound('email')
    
    return user
    
    