from typing import Optional, List, Dict

class CategoryViewmodel:
    category_id: str
    category_name: Optional[str]
    category_primary_color: str
    category_secondary_color: str
    
    def __init__(
        self, 
        category_id: str,
        category_name: Optional[str],
        category_primary_color: str,
        category_secondary_color: str
    ):
        self.category_id = category_id
        self.category_name = category_name
        self.category_primary_color = category_primary_color
        self.category_secondary_color = category_secondary_color
    
    def to_dict(self) -> dict:
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
            "category_primary_color": self.category_primary_color,
            "category_secondary_color": self.category_secondary_color
        }
    
class GetAllCategoriesViewmodel:
    categories_viewmodel_list: List[CategoryViewmodel]
    
    def __init__(self, categories: List[Dict]) -> None:
        categories_list = []
        for category in categories:
            category_viewmodel = CategoryViewmodel(
                category['_id'],
                category.get('category_name'),
                category['category_primary_color'],
                category['category_secondary_color']
            )
            categories_list.append(category_viewmodel)
        
        self.categories_viewmodel_list = categories_list
    
    def to_dict(self) -> dict:
        categories_list = [category_viewmodel.to_dict() for category_viewmodel in self.categories_viewmodel_list]
        return {
            "categories": categories_list,
            "message": "Todas as categorias retornadas com sucesso"
        }
