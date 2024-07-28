import pytest

from src.modules.delete_category_by_id.app.delete_category_by_id_viewmodel import DeleteCategoryByIdViewmodel

class Test_DeleteCategoryByIdViewmodel:

    def test_get_delete_category_by_id_viewmodel(self):
        expected = {
            'message': 'Categoria deletada com sucesso'
        }

        viewmodel = DeleteCategoryByIdViewmodel()

        assert viewmodel.to_dict() == expected