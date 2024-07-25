from typing import List, Optional
from datetime import date, time, datetime
from collections import defaultdict

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
            "task_date": self.task_date.strftime('%d/%m/%Y'),
            "task_hour": self.task_hour.isoformat(),
            "task_description": self.task_description,
            "task_local": self.task_local,
            "task_status": self.task_status
        }

class GetAllTasksViewmodel:
    tasks_viewmodel_list: List[TaskViewmodel]

    def __init__(self, tasks: List[dict]) -> None:
        tasks_list = []
        for task in tasks:
            task_date = datetime.strptime(task['task_date'], '%Y-%m-%d').date()
            task_hour = datetime.strptime(task['task_hour'], '%H:%M:%S').time()

            category_viewmodel = CategoryViewmodel(
                category_id=task['category']['category_id'],
                category_name=task['category']['category_name'],
                category_primary_color=task['category']['category_primary_color'],
                category_secondary_color=task['category']['category_secondary_color']
            ) if task.get('category') else None

            task_viewmodel = TaskViewmodel(
                task_id=task['task_id'],
                category=category_viewmodel,
                task_name=task['task_name'],
                task_date=task_date,
                task_hour=task_hour,
                task_description=task.get('task_description'),
                task_local=task.get('task_local'),
                task_status=task['task_status']
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
                date_key = task_viewmodel.task_date.strftime('%d/%m/%Y')
            
            tasks_by_date[date_key].append(task_viewmodel.to_dict())
        
        tasks = {date_key: tasks for date_key, tasks in tasks_by_date.items()}
        
        colors = []
        for task_viewmodel in self.tasks_viewmodel_list[:3]:
            colors.append(task_viewmodel.category.category_primary_color)
        
        dots = {}
        for task_viewmodel in self.tasks_viewmodel_list:
            task_date_str = task_viewmodel.task_date.isoformat()
            actual_date_key = current_day if task_date_str == current_day else task_date_str
            if actual_date_key not in dots:
                dots[actual_date_key] = {'dots': []}
                if actual_date_key == current_day:
                    dots[actual_date_key]['selected'] = True
            num_tasks = len(dots[actual_date_key]['dots']) + 1
            if num_tasks <= len(colors):
                dots[actual_date_key]['dots'].append({'key': f'dot{num_tasks}', 'color': colors[num_tasks - 1]})
        
        return {
            "message": "Task list retrieved successfully",
            "tasks": tasks,
            "dots": dots,
            "CurrentDay": current_day
        }
