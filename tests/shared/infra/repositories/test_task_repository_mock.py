from src.shared.domain.entities.task import Task
from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock

class Test_TaskRepositoryMock:
    def test_create_task(self):
        repo = TaskRepositoryMock()
        name = "Loteria"
        category_id = "123"
        user_id = "1"
        new_task = Task(
            task_id="123",
            user_id=user_id,
            category_id=category_id,
            task_name=name,
            task_date="2021-12-12",
            task_hour="12:00:00",
            task_description="Description for task 1",
            task_local="Local 1",
            task_status="ACTIVE",
        )
        task = repo.create_task(new_task)

        assert type(task) == Task
        assert task in repo.tasks
    
    def test_get_all_tasks(self):
        repo = TaskRepositoryMock()
        user_id = "1"

        tasks = repo.get_all_tasks(user_id)

        assert type(tasks) == list
        assert len(tasks) == len(repo.tasks)
    
    def test_delete_task(self):
        repo = TaskRepositoryMock()
        task_id = '1'

        repo.delete_task_by_id(task_id)

        assert task_id not in repo.tasks
    
    def test_get_task_by_id(self):
        repo = TaskRepositoryMock()
        task_id = '1'

        task = repo.get_task_by_id(task_id)

        assert task.task_id == task_id

    def test_update_task(self):
        repo = TaskRepositoryMock()
        task_id = '1'
        category_id = '1'
        task_name = 'Teste'
        task_date = '2021-01-01'
        task_hour = '12:00:00'
        task_description = 'Teste'
        task_local = 'Teste'
        task_status = 'ACTIVE'

        task = repo.update_task(
            task_id=task_id,
            category_id=category_id,
            task_name=task_name,
            task_date=task_date,
            task_hour=task_hour,
            task_description=task_description,
            task_local=task_local,
            task_status=task_status
        )

        assert task.task_id == task_id
        assert task.task_name == task_name
        assert task.task_date == task_date
        assert task.task_hour == task_hour
        assert task.task_description == task_description
        assert task.task_local == task_local
        assert task.task_status == task_status

    def test_get_task_by_day(self):
        repo = TaskRepositoryMock()
        task_date = '2021-12-12'

        tasks = repo.get_task_by_day(task_date)

        assert type(tasks) == list
        assert len(tasks) == 5
        assert tasks[0].task_date == task_date
    