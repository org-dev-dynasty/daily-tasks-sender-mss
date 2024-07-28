import pytest

from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.category_repository_mock import CategoryRepositoryMock
from src.modules.create_category.app.create_category_usecase import CreateCategoryUsecase
from src.modules.create_category.app.create_category_controller import CreateCategoryController

class Test_CreateCategoryController:

    def test_create_category_controller(self):
        repo = CategoryRepositoryMock()
        usecase = CreateCategoryUsecase(repo)
        controller = CreateCategoryController(usecase)
        
        print(f'os stage {Environments.get_envs().stage}')

        request = HttpRequest(body={
            'category_name': 'prova de os',
            'user_id': '1',
            'category_primary_color': '#000000',
            'category_secondary_color': '#FFFFFF'
        })

        response = controller(request)

        assert response.status_code == 201