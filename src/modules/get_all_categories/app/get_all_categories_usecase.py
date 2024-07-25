from src.shared.domain.irepositories.category_repository_interface import ICategoryRepository


class GetAllCategoriesUsecase:
  def __init__(self, repo: ICategoryRepository):
    self.repo = repo
    
  def __call__(self):
    categories = self.repo.get_all_categories()
    return categories