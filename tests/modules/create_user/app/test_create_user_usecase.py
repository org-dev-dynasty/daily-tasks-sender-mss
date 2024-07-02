import pytest

from src.shared.domain.entities.user import User
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem

class Test_CreateUserUsecase:

    def test_create_user_usecase(self):
        user = User(
            name="gabriel",
            email="gabriel@gmail.com",
            phone="11912345678",
            password="Teste@01",
            accepted_terms=True,
            accepted_notifications_email=True
        )
        repo = UserRepositoryMock()
        len_before = len(repo.users)
        usecase = CreateUserUsecase(repo=repo)

        new_user = usecase(user=user)

        assert type(new_user) == User
        assert new_user.name == 'gabriel'
        assert new_user.email == 'gabriel@gmail.com'
        assert new_user.phone == "11912345678"
        assert new_user.accepted_terms == True
        assert new_user.accepted_notifications_email == True
        assert len(repo.users) == len_before + 1

    def test_create_user_usecase_entity_error(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        with pytest.raises(EntityError):
            user = User(
                name="gabriel",
                email=None,
                phone="11912345678",
                password="Teste@01",
                accepted_terms=True,
                accepted_notifications_email=True
            )
            new_user = usecase(user)
    
    def test_create_user_duplicated_item(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        user = User(
            name="Merola", 
            email="merola.gay@gmail.com", 
            phone="11599999999", 
            password="Teste15@", 
            accepted_terms=True,
            accepted_notifications_email=True,
            user_id='1')
        
        with pytest.raises(DuplicatedItem):
            new_user = usecase(user)
