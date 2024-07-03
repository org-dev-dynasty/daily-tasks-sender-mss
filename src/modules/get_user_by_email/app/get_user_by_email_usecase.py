from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.controller_errors import MissingParameters

class GetUserByEmailUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo
    
    def __call__(self, email: str) -> User:
        if not email:
            raise MissingParameters("email")
        user_response = self.repo.get_user_by_email(email)
        return user_response
