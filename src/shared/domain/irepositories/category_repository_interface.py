from abc import ABC, abstractmethod
from src.shared.domain.entities.category import Category

class ICategoryRepository(ABC):
    @abstractmethod
    def get_all_categories(self, user_id: str) -> list:
        pass

    @abstractmethod
    def create_category(self, category: Category) -> Category:
        pass

    @abstractmethod
    def delete_category(self, category_id: str) -> None:
        pass