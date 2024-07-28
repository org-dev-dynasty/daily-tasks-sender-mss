from src.shared.domain.entities.category import Category
from src.shared.infra.repositories.category_repository_mock import CategoryRepositoryMock

class Test_CategoryRepositoryMock:
    def test_create_category(self):
        repo = CategoryRepositoryMock()
        name = "Loteria"
        primary_color = "#000000"
        secondary_color = "#FFFFFF"
        user_id = "1"
        new_category = Category(
            category_id="123",
            category_name=name,
            category_primary_color=primary_color,
            category_secondary_color=secondary_color,
            user_id=user_id
        )
        user = repo.create_category(new_category)

        assert type(user) == Category
        assert user in repo.categories
    
    def test_get_all_categories(self):
        repo = CategoryRepositoryMock()
        user_id = "1"

        categories = repo.get_all_categories(user_id)

        assert type(categories) == list
        assert len(categories) == len(repo.categories)
    
    def test_delete_category(self):
        repo = CategoryRepositoryMock()
        category_Id = '1'

        repo.delete_category(category_Id)

        assert category_Id not in repo.categories
    