from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.modules.get_user_by_email.app.get_user_by_email_usecase import GetUserByEmailUsecase


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
        
        user_exists = self.repo.get_user_by_email(user.email)
        
        if user_exists is not None:
            raise DuplicatedItem('email')

        user.email = user.email.lower()
        print("AQUI TA CHAMANDO O REPO DENTRO DO USECASE " + user.to_dict())
        user_response = self.repo.create_user(user)
        return user_response
