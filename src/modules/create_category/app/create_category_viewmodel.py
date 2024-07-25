from src.shared.domain.entities.category import Category

class CreateCategoryViewmodel:
    def __init__(self):
        pass

    def to_dict(self, category: Category):
        return {
            "category": category.to_dict(),
            "message": "Category created successfully"
        }
