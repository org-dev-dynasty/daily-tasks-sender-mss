from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError

class ChangePasswordUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo
    
    def execute(self, oldPassword: str, newPassword: str, access_token: str):
        if not User.validate_password(oldPassword):
            raise EntityError('oldPassword')
        if not User.validate_password(newPassword):
            raise EntityError('newPassword')
        if len(access_token) == 0 or access_token == "":
            raise EntityError('access_token')
        
        response = self.repo.change_password(oldPassword, newPassword, access_token)
        return response