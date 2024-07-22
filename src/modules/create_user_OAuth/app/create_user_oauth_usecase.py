from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class CreateUserOAuthUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user: User) -> dict:
        if not user.name:
            raise EntityError("name")
        if not user.email:
            raise EntityError("email")
        
        user.email = user.email.lower()
        user_response = self.repo.create_user(user)
        return user_response
        

