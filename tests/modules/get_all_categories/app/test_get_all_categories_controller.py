from src.modules.get_all_categories.app.get_all_categories_controller import GetAllCategoriesController
from src.modules.get_all_categories.app.get_all_categories_usecase import GetAllCategoriesUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.category_repository_mock import CategoryRepositoryMock


class Test_GetAllCategoriesController:

    def test_get_all_categories_controller(self):
        repo = CategoryRepositoryMock()
        usecase = GetAllCategoriesUsecase(repo)
        controller = GetAllCategoriesController(usecase)
        request = HttpRequest()

        response = controller(request)

        assert response.status_code == 200