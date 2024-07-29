from src.shared.domain.entities.task import Task


class GetAllInactivesTasksViewmodel:
    message: str
    tasks: list[Task]

    def __init__(self, message: str):
        self.message = message


    def to_dict(self, tasks: list[Task]):
        tasksList = []
        for task in tasks:
            tasksList.append(task.to_dict())

        return {
            "message": self.message,
            "tasks": tasksList
        }