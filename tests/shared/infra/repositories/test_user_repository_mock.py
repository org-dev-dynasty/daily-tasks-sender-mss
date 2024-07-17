from src.shared.domain.entities.user import User
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_UserRepositoryMock:
    def test_create_user(self):
        repo = UserRepositoryMock()
        name = "Jorge"
        email = "jorgin21221@gmail.com"
        phone = "11917283748"
        password = "Teste123@"
        accepted_terms = True
        accepted_notifications = False
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=password,
            accepted_terms=accepted_terms,
            accepted_notifications_email=accepted_notifications
        )
        user = repo.create_user(new_user)

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
