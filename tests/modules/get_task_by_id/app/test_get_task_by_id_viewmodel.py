from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock
from src.modules.get_task_by_id.app.get_task_by_id_viewmodel import GetTaskByIdViewmodel


class Test_GetProductViewmodel:

    def test_get_product_viewmodel(self):
        repo = TaskRepositoryMock()

        task = repo.tasks[0]

        task_viewmodel = GetTaskByIdViewmodel(task).to_dict()

        excepted = {
            "task": {
                "task_id": "1",
                "task_name": 'TaskUm',
                "task_date": "2021-12-12",
                "task_hour": "12:00:00",
                "task_description": "Description for task 1",
                "task_local": "Local 1",
                "task_status": "ACTIVE"
            },
            'message': 'the task was retrieved'
        }

        assert task_viewmodel == excepted
