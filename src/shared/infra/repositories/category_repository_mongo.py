from src.shared.domain.irepositories.category_repository_interface import ICategoryRepository
from src.shared.infra.repositories.database.mongodb.category_collection import get_category_collection

class CategoryRepositoryMongo(ICategoryRepository):

    def __init__(self, mongo_url: str):
        self.collection = get_category_collection(mongo_url)
    
    def get_all_categories(self, user_id: str) -> list:
        categories = []
        for category in self.collection.find({"user_id": user_id}):
            categories.append(category)
        return categories
    
    def create_category(self, category: dict) -> dict:
        self.collection.insert_one(category)
        return category
    
    def delete_category(self, category_id: str) -> None:
        self.collection.delete_one({"_id": category_id})
