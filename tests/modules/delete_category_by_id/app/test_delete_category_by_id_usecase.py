import pytest
from src.shared.domain.entities.category import Category
from src.modules.delete_category_by_id.app.delete_category_by_id_usecase import DeleteCategoryByIdUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.category_repository_mock import CategoryRepositoryMock

class TestDeleteCategoryByIdUsecase:

    def test_delete_category_by_id_usecase(self):
        repo_category = CategoryRepositoryMock()
        usecase = DeleteCategoryByIdUsecase(repo_category)
        len_before = len(repo_category.categories)

        category_id = "1"
        usecase.execute(category_id) 
        len_after = len_before - 1
        assert len(repo_category.categories) == len_after
        assert all(category.category_id != category_id for category in repo_category.categories)

    def test_delete_category_by_id_usecase_with_invalid_category_id(self):
        repo_category = CategoryRepositoryMock()
        usecase = DeleteCategoryByIdUsecase(repo_category)

        with pytest.raises(EntityError):
            usecase.execute(None)
    