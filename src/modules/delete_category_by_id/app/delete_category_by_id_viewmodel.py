class DeleteCategoryByIdViewmodel:

    def __init__(self):
        pass

    def to_dict(self) -> dict:
        return {
            "message": "the category was deleted successfully"
        }
