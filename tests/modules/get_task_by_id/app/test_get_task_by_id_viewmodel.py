from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock
from src.modules.get_task_by_id.app.get_task_by_id_viewmodel import GetTaskByIdViewmodel


class Test_GetProductViewmodel:

    def test_get_task_by_id_viewmodel(self):
        repo = TaskRepositoryMock()

        task = repo.tasks[0]

        task_viewmodel = GetTaskByIdViewmodel(task).to_dict()

        expected = {
            "task": {
                "task_id": "1",
                "category": {
                    "category_id": "1",
                    "category_name": "Categoria 1",
                    "category_primary_color": "#123456",
                    "category_secondary_color": "#654321"
                },
                "task_name": 'TaskUm',
                "task_date": "2021-12-12",
                "task_hour": "12:00:00",
                "task_description": "Description for task 1",
                "task_local": "Local 1",
                "task_status": "ACTIVE"
            },
            "message": "Task retornada com sucesso"
        }

        assert task_viewmodel == expected