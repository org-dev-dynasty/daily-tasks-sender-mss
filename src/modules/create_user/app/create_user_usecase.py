from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user: User) -> User:
        if not user.name:
            raise EntityError("name")
        if not user.email:
            raise EntityError("email")
        if not user.password:
            raise EntityError("password")
        if not user.accepted_terms:
            raise EntityError("accepted_terms")
        
        user.email = user.email.lower()
        user_response = self.repo.create_user(user)
        print('user_response USECASE: ' + str(user_response))
        return user_response
        

