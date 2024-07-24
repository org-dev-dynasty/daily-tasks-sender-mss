from abc import ABC, abstractmethod

class ICategoryRepository(ABC):
    @abstractmethod
    def get_all_categories(self, user_id: str) -> list:
        pass

    @abstractmethod
    def create_category(self, category: dict) -> dict:
        pass

    @abstractmethod
    def delete_category(self, category_id: str) -> None:
        pass
