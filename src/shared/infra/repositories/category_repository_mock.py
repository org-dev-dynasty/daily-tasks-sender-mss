from src.shared.domain.irepositories.category_repository_interface import ICategoryRepository
from src.shared.domain.entities.category import Category

class CategoryRepositoryMock(ICategoryRepository):
    def __init__(self):
        self.categories = [
            Category(category_name="CategoryUm", user_id="1", category_primary_color="#000000", category_secondary_color="#FFFFFF", category_id="1"),
            Category(category_name="CategoryDois", user_id="1", category_primary_color="#000000", category_secondary_color="#FFFFFF", category_id="2"),
            Category(category_name="CategoryTres", user_id="1", category_primary_color="#000000", category_secondary_color="#FFFFFF", category_id="3"),
            Category(category_name="CategoryQuatro", user_id="1", category_primary_color="#000000", category_secondary_color="#FFFFFF", category_id="4"),
            Category(category_name="CategoryCinco", user_id="1", category_primary_color="#000000", category_secondary_color="#FFFFFF", category_id="5"),
        ]
    
    def get_all_categories(self, user_id: str) -> list:
        return [category for category in self.categories if category.user_id == user_id]
    
    def create_category(self, category: Category) -> Category:
        self.categories.append(category)
        return category
    
    def delete_category(self, category_id: str) -> None:
        category = self.get_category_by_id(category_id)
        if category:
            self.categories.remove(category)
