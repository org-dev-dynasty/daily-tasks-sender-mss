import pytest

from src.modules.confirm_user_email.app.confirm_user_email_usecase import ConfirmUserEmailUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_ConfirmUserEmailUsecase:

    def test_confirm_user_email_usecase(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserEmailUsecase(repo)
        
        user = usecase(email="digao@gmail.com", verification_code="123456")
        
        assert user.name == repo.users[0].name
        
    def test_confirm_user_email_usecase_with_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserEmailUsecase(repo)
        
        with pytest.raises(EntityError):
            usecase(email=0, verification_code="123456")
            
    def test_confirm_user_email_usecase_with_invalid_verification_code(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserEmailUsecase(repo)
        
        with pytest.raises(EntityError):
            usecase(email="digao@gmail.com", verification_code="")
            
    def test_confirm_user_email_usecase_with_no_items_found(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserEmailUsecase(repo)
        
        with pytest.raises(NoItemsFound):
            usecase(email="email@email.com", verification_code="123456")
