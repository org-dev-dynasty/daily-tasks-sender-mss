import pytest

from src.modules.create_category.app.create_category_viewmodel import CreateCategoryViewmodel
from src.shared.domain.entities.category import Category

class Test_CreateCategoryViewmodel:

    def test_get_category_viewmodel(self):
        category = Category(
            category_id='1',
            category_name='Category',
            user_id='1',
            category_primary_color='#000000',
            category_secondary_color='#FFFFFF',
        )

        expected = {
            "message": "Category created successfully"
        }

        viewmodel = CreateCategoryViewmodel()

        assert viewmodel.to_dict() == expected
