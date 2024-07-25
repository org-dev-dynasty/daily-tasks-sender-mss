from src.shared.domain.irepositories.category_repository_interface import ICategoryRepository
from src.shared.infra.repositories.database.mongodb.category_collection import get_category_collection
from src.shared.domain.entities.category import Category

class CategoryRepositoryMongo(ICategoryRepository):

    def __init__(self, mongo_url: str):
        self.collection = get_category_collection(mongo_url)
    
    def get_all_categories(self, user_id: str) -> list:
        categories = []
        for category in self.collection.find({"user_id": user_id}):
            categories.append(category)
        return categories
    
    def create_category(self, category: Category) -> Category:
        self.collection.insert_one(category.to_dict())
        return category
    
    def delete_category(self, category_id: str) -> None:
        self.collection.delete_one({"_id": category_id})
