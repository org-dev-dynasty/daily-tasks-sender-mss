from src.shared.domain.entities.task import Task

class TaskViewmodel:
    task_name: str
    task_date: str
    task_hour: str
    task_status: str

    def __init__(self, task: Task):
        self.task_id = task.task_id
        self.task_name = task.task_name
        self.task_date = task.task_date
        self.task_hour = task.task_hour
        self.task_status = task.task_status
    
    def to_dict(self):
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_date': self.task_date,
            'task_hour': self.task_hour,
            'task_status': self.task_status,
        }

class CreateTaskViewmodel:
    task: TaskViewmodel

    def __init__(self, task: Task):
        self.task = TaskViewmodel(task)

    def to_dict(self):
        return {
            'task': self.task.to_dict(),
            'message': 'the task was created'
        }