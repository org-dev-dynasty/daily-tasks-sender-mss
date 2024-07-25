from src.shared.domain.irepositories.category_repository_interface import ICategoryRepository
from src.shared.helpers.errors.domain_errors import EntityError

class DeleteCategoryByIdUsecase:
    def __init__(self, task_repo: ICategoryRepository):
        self.task_repo = task_repo

    def __call__(self, category_id: str) -> None:
        if not category_id:
            raise EntityError("category_id")
        try:
            self.task_repo.delete_category(category_id=category_id)
        except Exception as e:
            raise EntityError("category_id") from e
