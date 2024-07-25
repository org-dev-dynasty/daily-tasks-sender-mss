from src.shared.domain.entities.category import Category
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.domain.irepositories.category_repository_interface import ICategoryRepository


class CreateCategoryUsecase:
    def __init__(self, repo: ICategoryRepository):
        self.repo = repo
    
    def execute(self, category: Category):
        if not category.user_id:
            raise EntityError('user_id')
        if not category.category_primary_color:
            raise EntityError('category_primary_color')
        if not category.category_secondary_color:
            raise EntityError('category_secondary_color')
        
        response = self.repo.create_category(category)
        return response
