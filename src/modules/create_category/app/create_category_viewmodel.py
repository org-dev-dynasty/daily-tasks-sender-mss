from src.shared.domain.entities.category import Category

class CreateCategoryViewmodel:
    def __init__(self):
        pass

    def to_dict(self):
        return {
            "message": "Category created successfully"
        }
