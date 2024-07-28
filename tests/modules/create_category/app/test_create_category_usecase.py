import pytest

from src.shared.domain.entities.category import Category
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.category_repository_mock import CategoryRepositoryMock
from src.modules.create_category.app.create_category_usecase import CreateCategoryUsecase

class Test_CreateCategoryUsecase:

    def test_create_category_usecase(self):
        category = Category(
            user_id='1',
            category_id='1',
            category_name='Category',
            category_primary_color='#000000',
            category_secondary_color='#FFFFFF',
        )
        repo = CategoryRepositoryMock()
        len_before = len(repo.categories)
        usecase = CreateCategoryUsecase(repo)

        new_category = usecase.execute(category)

        assert type(new_category) == Category
        assert new_category.category_name == 'Category'
        assert new_category.category_primary_color == '#000000'
        assert new_category.category_secondary_color == '#FFFFFF'
        assert len(repo.categories) == len_before + 1
    
    def test_create_category_usecase_error(self):
        repo = CategoryRepositoryMock()
        usecase = CreateCategoryUsecase(repo)

        with pytest.raises(EntityError):
            category = Category(
                user_id='1',
                category_id='1',
                category_name=None,
                category_primary_color=None,
                category_secondary_color='#FFFFFF',
            )
            usecase.execute(category)