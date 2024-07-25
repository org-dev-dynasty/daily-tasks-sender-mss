import pytest

from src.modules.create_task.app.create_task_viewmodel import CreateTaskViewmodel
from src.shared.domain.entities.task import Task

class Test_CreateTaskViewmodel:

    def test_get_task_viewmodel(self):
        task = Task(
            task_name='Task',
            category_id='1',
            user_id='1',
            task_description='Description of task 1',
            task_local='Local of task 1',
            task_date='2021-12-31',
            task_hour='12:00:00',
            task_status='ACTIVE'
        )

        expected = {
            'task': {
                'task_id': task.task_id,
                'task_name': task.task_name,
                'task_date': task.task_date,
                'task_hour': task.task_hour,
                'task_status': task.task_status,
            },
            'message': 'the task was created'
        }

        viewmodel = CreateTaskViewmodel(task)

        assert viewmodel.to_dict() == expected