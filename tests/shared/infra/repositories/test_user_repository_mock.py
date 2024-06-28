from src.shared.domain.entities.user import User
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_UserRepositoryMock:
    
    def test_get_all_users(self):
        repo = UserRepositoryMock()
        users = repo.get_all_users()

        assert type(users) == list
        assert all([type(user) == User for user in users])
        assert len(users) == len(repo.users)
        assert users == repo.users

    def test_create_user(self):
        repo = UserRepositoryMock()
        name = "Jorge"
        email = "jorgin@gmail.com"
        phone = "11917283748"
        password = "Teste123@"
        accepted_terms = True
        accepted_notifications = False

        user = repo.create_user(name, email, phone, password, accepted_terms, accepted_notifications)

        assert type(user) == User
        assert user in repo.users
    
    def test_login(self):
        repo = UserRepositoryMock()
        email = "merola.gay@gmail.com"
        password = "Teste15@"

        user = repo.login(email, password)

        assert type(user) == User
        assert user.email == email
    
    def test_get_user_by_id(self):
        repo = UserRepositoryMock()
        user_id = '1'

        user = repo.get_user_by_id(user_id)

        assert type(user) == User
        assert user.user_id == user_id
        assert user in repo.users
        assert user.email == "merola.gay@gmail.com"
        assert user.phone == "11599999999"
        assert user.password == "Teste15@"
        assert user.name == "Merola"
