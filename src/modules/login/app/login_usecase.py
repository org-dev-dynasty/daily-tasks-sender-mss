from src.shared.domain.irepositories.user_repository_interface import IUserRepository


class LoginUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, email, password):
        login = self.repo.login(email, password)
        return login
