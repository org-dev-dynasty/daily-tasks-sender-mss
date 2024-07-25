from typing import List, Optional
from datetime import date, time, timedelta, datetime
from collections import defaultdict

from src.shared.domain.entities.task import Task

class TaskViewmodel:
    task_id: str
    category_id: str
    task_name: str
    task_date: date
    task_hour: time
    task_description: Optional[str]
    task_local: Optional[str]
    task_status: str

    def __init__(self, task_id: str, category_id: str, task_name: str, task_date: date, task_hour: time, task_description: Optional[str], task_local: Optional[str], task_status: str) -> None:
        self.task_id = task_id
        self.category_id = category_id
        self.task_name = task_name
        self.task_date = task_date
        self.task_hour = task_hour
        self.task_description = task_description
        self.task_local = task_local
        self.task_status = task_status
    
    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "category_id": self.category_id,
            "task_name": self.task_name,
            "task_date": self.task_date,
            "task_hour": self.task_hour,
            "task_description": self.task_description,
            "task_local": self.task_local,
            "task_status": self.task_status
        }

class GetAllTasksViewmodel:
    tasks_viewmodel_list: List[TaskViewmodel]

    def __init__(self, tasks: List[Task]) -> None:
        tasks_list = []
        for task in tasks:
            task_viewmodel = TaskViewmodel(
                task.task_id,
                task.category_id,
                task.task_name,
                task.task_date,
                task.task_hour,
                task.task_description,
                task.task_local,
                task.task_status
            )
            tasks_list.append(task_viewmodel)
        
        self.tasks_viewmodel_list = tasks_list
    
    def to_dict(self) -> dict:
        tasks_by_date = defaultdict(list)
        current_day = datetime.strptime(task_date, "%Y-%m-%d").date()
        
        for task_viewmodel in self.tasks_viewmodel_list:
            task_date = task_viewmodel.task_date
            if task_date == current_day:
                date_key = "Hoje"
            elif task_date == current_day + timedelta(days=1):
                date_key = "Amanhã"
            else:
                date_key = task_date
            
            tasks_by_date[date_key].append(task_viewmodel.to_dict())
        
        tasks = {date_key: tasks for date_key, tasks in tasks_by_date.items()}
        
        colors = ['red', 'blue', 'green']
        dots = {}
        for date_key, task_list in tasks_by_date.items():
            task_date_str = task_list[0]["task_date"]  # Usando a data da primeira tarefa na lista
            num_tasks = min(len(task_list), 3)
            dots[task_date_str] = {'dots': [{'key': f'dot{i+1}', 'color': colors[i]} for i in range(num_tasks)]}
        
        return {
            "message": "Task list retrieved successfully",
            "tasks": tasks,
            "dots": dots,
            "CurrentDay": current_day.isoformat()
        }