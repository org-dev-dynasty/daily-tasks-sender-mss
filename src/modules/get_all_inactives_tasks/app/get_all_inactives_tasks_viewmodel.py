from src.shared.domain.entities.task import Task

class CategoryViewmodel:
    def __init__(self, category_id: str, category_name: str, category_primary_color: str, category_secondary_color: str):
        self.category_id = category_id
        self.category_name = category_name
        self.category_primary_color = category_primary_color
        self.category_secondary_color = category_secondary_color

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
            "category_primary_color": self.category_primary_color,
            "category_secondary_color": self.category_secondary_color,
        }


class TaskViewmodel:
    def __init__(self, task_id: str, category: CategoryViewmodel, task_name: str, task_date: str, task_hour: str, task_description: str, task_local: str, task_status: str):
        self.task_id = task_id
        self.category = category
        self.task_name = task_name
        self.task_date = task_date
        self.task_hour = task_hour
        self.task_description = task_description
        self.task_local = task_local
        self.task_status = task_status

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "category": self.category.to_dict(),
            "task_name": self.task_name,
            "task_date": self.task_date,
            "task_hour": self.task_hour,
            "task_description": self.task_description,
            "task_local": self.task_local,
            "task_status": self.task_status,
        }


class GetAllInactivesTasksViewmodel:
    def __init__(self, tasks_data: list[dict]):
        self.message = "Tasks inativas retornadas com sucesso"
        self.tasks = self.convert_to_task_viewmodels(tasks_data)

    def convert_to_task_viewmodels(self, tasks_data: list[dict]) -> list[TaskViewmodel]:
        tasks = []
        for task_data in tasks_data:
            category_data = task_data['category']
            category = CategoryViewmodel(
                category_id=category_data['category_id'], 
                category_name=category_data['category_name'], 
                category_primary_color=category_data['category_primary_color'], 
                category_secondary_color=category_data['category_secondary_color']
            )
            
            task = TaskViewmodel(
                task_id=task_data['task_id'],
                category=category,
                task_name=task_data['task_name'],
                task_date=task_data['task_date'],
                task_hour=task_data['task_hour'],
                task_description=task_data['task_description'],
                task_local=task_data['task_local'],
                task_status=task_data['task_status']
            )
            tasks.append(task)
        return tasks

    def to_dict(self):
        tasks_list = [task.to_dict() for task in self.tasks]
        return {
            "message": self.message,
            "tasks": tasks_list
        }