import pytest

from src.modules.delete_category_by_id.app.delete_category_by_id_controller import DeleteCategoryByIdController
from src.modules.delete_category_by_id.app.delete_category_by_id_usecase import DeleteCategoryByIdUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.category_repository_mock import CategoryRepositoryMock

class Test_DeleteCategoryByIdController:

    def test_delete_category_by_id_controller(self):
        repo = CategoryRepositoryMock()
        usecase = DeleteCategoryByIdUsecase(repo)
        controller = DeleteCategoryByIdController(usecase)
        request = HttpRequest(query_params={"category_id": repo.categories[0].category_id})

        response = controller(request)

        assert response.status_code == 200