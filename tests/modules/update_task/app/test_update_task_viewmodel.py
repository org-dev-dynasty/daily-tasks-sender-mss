import pytest

from src.modules.update_task.app.update_task_viewmodel import UpdateTaskViewmodel

class Test_UpdateTaskViewmodel:

    def test_get_update_task_viewmodel(self):
        expected = {
            "message": "task updated"
        }

        viewmodel = UpdateTaskViewmodel()

        assert viewmodel.to_dict() == expected