from src.shared.domain.irepositories.category_repository_interface import ICategoryRepository


class GetAllCategoriesUsecase:
  def __init__(self, repo: ICategoryRepository):
    self.repo = repo
    
  def execute(self, user_id: str):
    categories = self.repo.get_all_categories(user_id)
    return categories