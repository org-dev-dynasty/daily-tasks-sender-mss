from src.modules.login.app.login_usecase import LoginUsecase
from src.shared.infra.repositories.user.user_repository_mock import UserRepositoryMock


class Test_LoginUsecase:

    def test_login_usecase(self):
        repo_mock = UserRepositoryMock()
        usecase = LoginUsecase(repo_mock)

        all_users_list_returned = usecase.execute(email=repo_mock.users[0].email, password=repo_mock.users[0].password)

        assert all_users_list_returned == True
