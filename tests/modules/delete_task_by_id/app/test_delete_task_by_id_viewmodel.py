import pytest

from src.modules.delete_task_by_id.app.delete_task_by_id_viewmodel import DeleteTaskByIdViewmodel

class Test_DeleteTaskByIdViewmodel:

    def test_get_delete_task_by_id_viewmodel(self):
        expected = {
            "message": "the task was deleted successfully"
        }

        viewmodel = DeleteTaskByIdViewmodel()

        assert viewmodel.to_dict() == expected