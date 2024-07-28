from src.modules.get_all_categories.app.get_all_categories_usecase import GetAllCategoriesUsecase
from src.shared.infra.repositories.category_repository_mock import CategoryRepositoryMock


class Test_GetAllCategoriesUsecase:

    def test_get_all_categories_usecase(self):
        repo = CategoryRepositoryMock()
        usecase = GetAllCategoriesUsecase(repo)
        user_id = '1'

        category = usecase.execute(user_id=user_id)

        assert type(category) == list
        assert category[0].category_id == '1'
    