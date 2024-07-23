from typing import Optional
from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.domain_errors import EntityError


class CreateUserOAuthUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str, name: str, phone: Optional[str]) -> dict:
        if not User.validate_email(email):
            raise EntityError("email")
        if not User.validate_name(name):
            raise EntityError("name")
        
        base_pwd = Environments.get_envs().base_pwd_cognito
        
        user = User(name=name, email=email, phone=phone, password=base_pwd, accepted_terms=True, accepted_notifications_email=True)
        tokens_response = self.repo.create_user_oauth(user)
        return tokens_response
        

