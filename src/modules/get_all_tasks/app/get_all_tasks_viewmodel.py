from typing import List, Optional
from datetime import date, time
from collections import defaultdict

from src.shared.domain.entities.task import Task
from src.shared.domain.entities.category import Category


class CategoryViewmodel:
    category_id: str
    category_name: str
    category_primary_color: str
    category_secondary_color: str

    def __init__(self, category_id: str, category_name: str, category_primary_color: str, category_secondary_color: str) -> None:
        self.category_id = category_id
        self.category_name = category_name
        self.category_primary_color = category_primary_color
        self.category_secondary_color = category_secondary_color
    
    def to_dict(self) -> dict:
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
            "category_primary_color": self.category_primary_color,
            "category_secondary_color": self.category_secondary_color
        }

class TaskViewmodel:
    task_id: str
    category: CategoryViewmodel
    task_name: str
    task_date: date
    task_hour: time
    task_description: Optional[str]
    task_local: Optional[str]
    task_status: str

    def __init__(self, task_id: str, category: CategoryViewmodel, task_name: str, task_date: date, task_hour: time, task_description: Optional[str], task_local: Optional[str], task_status: str) -> None:
        self.task_id = task_id
        self.category = category
        self.task_name = task_name
        self.task_date = task_date
        self.task_hour = task_hour
        self.task_description = task_description
        self.task_local = task_local
        self.task_status = task_status
    
    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "category": self.category.to_dict() if self.category else None,
            "task_name": self.task_name,
            "task_date": self.task_date.isoformat(),
            "task_hour": self.task_hour.isoformat(),  
            "task_description": self.task_description,
            "task_local": self.task_local,
            "task_status": self.task_status
        }

class GetAllTasksViewmodel:
    tasks_viewmodel_list: List[TaskViewmodel]

    def __init__(self, tasks: List[Task]) -> None:
        tasks_list = []
        for task in tasks:
            category_viewmodel = CategoryViewmodel(
                category_id=task.category.category_id,
                category_name=task.category.category_name,
                category_primary_color=task.category.category_primary_color,
                category_secondary_color=task.category.category_secondary_color
            ) if task.category else None

            task_viewmodel = TaskViewmodel(
                task_id=task.task_id,
                category=category_viewmodel,
                task_name=task.task_name,
                task_date=task.task_date,
                task_hour=task.task_hour,
                task_description=task.task_description,
                task_local=task.task_local,
                task_status=task.task_status
            )
            tasks_list.append(task_viewmodel)
        
        self.tasks_viewmodel_list = tasks_list
    
    def to_dict(self) -> dict:
        tasks_by_date = defaultdict(list)
        current_day = date.today().isoformat()
        
        for task_viewmodel in self.tasks_viewmodel_list:
            task_date_str = task_viewmodel.task_date.isoformat()
            if task_date_str == current_day:
                date_key = "Hoje"
            else:
                date_key = task_date_str
            
            tasks_by_date[date_key].append(task_viewmodel.to_dict())
        
        tasks = {date_key: tasks for date_key, tasks in tasks_by_date.items()}
        
        colors = ['red', 'blue', 'green']
        dots = {}
        for date_key, task_list in tasks_by_date.items():
            num_tasks = min(len(task_list), len(colors))
            dots[date_key] = {'dots': [{'key': f'dot{i+1}', 'color': colors[i]} for i in range(num_tasks)]}
        
        return {
            "message": "Task list retrieved successfully",
            "tasks": tasks,
            "dots": dots,
            "CurrentDay": current_day
        }
