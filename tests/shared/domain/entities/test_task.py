import pytest
from datetime import date, time
from src.shared.domain.entities.task import Task
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.domain.enums.status_enum import STATUS


class Test_Task:
    def test_entity_correctly(self):
        task = Task(task_id=1, task_name="Complete project", task_description="Finish the project by EOD", task_local="Office", task_status=STATUS.ACTIVE)

        assert type(task) == Task
        assert task.task_id == 1
        assert task.task_name == "Complete project"
        assert task.task_description == "Finish the project by EOD"
        assert task.task_local == "Office"
        assert task.task_status == STATUS.ACTIVE

    def test_entity_incorrectly_task_name(self):
        with pytest.raises(EntityError):
            Task(task_id=2, task_name="Complete project 123", task_description="Finish the project by EOD", task_local="Office", task_status=STATUS.ACTIVE)
        with pytest.raises(EntityError):
            Task(task_id=3, task_name="", task_description="Finish the project by EOD", task_local="Office", task_status=STATUS.ACTIVE)
        with pytest.raises(EntityError):
            Task(task_id=4, task_name=None, task_description="Finish the project by EOD", task_local="Office", task_status=STATUS.ACTIVE)
        with pytest.raises(EntityError):
            Task(task_id=5, task_name="a", task_description="Finish the project by EOD", task_local="Office", task_status=STATUS.ACTIVE)

    def test_entity_incorrectly_task_description(self):
        with pytest.raises(EntityError):
            Task(task_id=6, task_name="Meeting", task_description="Meeting with client 123", task_local="Office", task_status=STATUS.ACTIVE)
        with pytest.raises(EntityError):
            Task(task_id=7, task_name="Meeting", task_description="", task_local="Office", task_status=STATUS.ACTIVE)
        with pytest.raises(EntityError):
            Task(task_id=8, task_name="Meeting", task_description=None, task_local="Office", task_status=STATUS.ACTIVE)
        with pytest.raises(EntityError):
            Task(task_id=9, task_name="Meeting", task_description="a", task_local="Office", task_status=STATUS.ACTIVE)

    def test_entity_incorrectly_task_local(self):
        with pytest.raises(EntityError):
            Task(task_id=10, task_name="Presentation", task_description="Present the quarterly report", task_local="Room 123", task_status=STATUS.ACTIVE)
        with pytest.raises(EntityError):
            Task(task_id=11, task_name="Presentation", task_description="Present the quarterly report", task_local="", task_status=STATUS.ACTIVE)
        with pytest.raises(EntityError):
            Task(task_id=12, task_name="Presentation", task_description="Present the quarterly report", task_local=None, task_status=STATUS.ACTIVE)
        with pytest.raises(EntityError):
            Task(task_id=13, task_name="Presentation", task_description="Present the quarterly report", task_local="a", task_status=STATUS.ACTIVE)

