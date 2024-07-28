from src.modules.get_all_categories.app.get_all_categories_viewmodel import GetAllCategoriesViewmodel


class Test_GetAllCategoriesViewmodel:

    def test_get_all_categories_viewmodel(self):
        expected = {
            "categories": [
                {
                    "category_id": "1",
                    "category_name": "Category 1",
                    "category_primary_color": "#000000",
                    "category_secondary_color": "#ffffff"
                },
                {
                    "category_id": "2",
                    "category_name": "Category 2",
                    "category_primary_color": "#ffffff",
                    "category_secondary_color": "#000000"
                }
            ],
            "message": "Todas as categorias retornadas com sucesso"
        }

        viewmodel = GetAllCategoriesViewmodel([
                {
                    "_id": "1",
                    "category_name": "Category 1",
                    "category_primary_color": "#000000",
                    "category_secondary_color": "#ffffff"
                },
                {
                    "_id": "2",
                    "category_name": "Category 2",
                    "category_primary_color": "#ffffff",
                    "category_secondary_color": "#000000"
                }
            ])

        assert viewmodel.to_dict() == expected
    