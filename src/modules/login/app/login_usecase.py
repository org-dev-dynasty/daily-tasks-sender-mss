from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import InvalidCredentials, NoItemsFound


class LoginUseCase:
    def __init__(self, repo: IUserRepository):
        self.user_repository = repo

    def __call__(self, email: str, password: str) -> dict:
        if not User.validate_email(email):
            raise EntityError('email')

        if not User.validate_password(password):
            raise EntityError('password')
        
        print(f'chegou no usecase {email} {password}')
        
        user = self.user_repository.get_user_by_email(email)
        if user is None:
            raise NoItemsFound('user')

        data = self.user_repository.login(email, password)
        if data is None:
            raise InvalidCredentials('user')

        return data
