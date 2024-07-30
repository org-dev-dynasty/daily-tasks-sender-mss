from src.shared.domain.entities.task import Task
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.infra.dto.task_mongo_dto import TaskMongoDTO
from src.shared.infra.repositories.database.mongodb.task_collection import get_tasks_collection
from typing import List, Optional, Dict, Any
from datetime import date, time


class TaskRepositoryMongo(ITaskRepository):

    def __init__(self, mongo_url: str):
        self.collection = get_tasks_collection(mongo_url)

    def create_task(self, task: Task) -> Task:
        self.collection.insert_one(task.to_dict())
        return task

    def get_task_by_id(self, task_id: str) -> dict:
        try:
            task = self.collection.aggregate([
                {
                    '$match': {
                        '_id': task_id
                    }
                },
                {
                    '$lookup': {
                        'from': 'categories',
                        'localField': 'category_id',
                        'foreignField': '_id',
                        'as': 'category'
                    }
                }
            ])

            taskList = list(task)

            if not taskList:
                return None

            task = taskList[0]

            category = task.get('category')
            task_viewmodel = {
                'task_id': str(task.get('_id')),
                'category': {
                    'category_id': str(category[0].get('_id')),
                    'category_name': category[0].get('category_name'),
                    'category_primary_color': category[0].get('category_primary_color'),
                    'category_secondary_color': category[0].get('category_secondary_color')
                },
                'task_name': task.get('task_name'),
                'task_date': task.get('task_date'),
                'task_hour': task.get('task_hour'),
                'task_description': task.get('task_description', None),
                'task_local': task.get('task_local', None),
                'task_status': task.get('task_status')
            }

            print(task_viewmodel)

            return task_viewmodel
        except Exception as e:
            print(f"Error: {e}")
            return ValueError(f"Error on get task by id, err: {e}")

    def get_all_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        allTasks = self.collection.aggregate([
            {
                '$match': {
                    'user_id': user_id
                }
            },
            {
                '$lookup': {
                    'from': 'categories',
                    'localField': 'category_id',
                    'foreignField': '_id',
                    'as': 'category'
                }
            }
        ])

        # Converter o cursor em uma lista
        allTasksList = list(allTasks)

        print("allTasks:")
        for task in allTasksList:
            print(task)

        tasks = []
        for task in allTasksList:
            category = task.get('category')
            task_viewmodel = {
                'task_id': str(task.get('_id')),
                'category': {
                    'category_id': str(category[0].get('_id')),
                    'category_name': category[0].get('category_name'),
                    'category_primary_color': category[0].get('category_primary_color'),
                    'category_secondary_color': category[0].get('category_secondary_color')
                },
                'task_name': task.get('task_name'),
                'task_date': task.get('task_date'),
                'task_hour': task.get('task_hour'),
                'task_description': task.get('task_description', None),
                'task_local': task.get('task_local', None),
                'task_status': task.get('task_status')
            }
            tasks.append(task_viewmodel)

        print(tasks)
        
        return tasks

    def get_all_inactives_tasks(self, user_id: str) -> List[dict]:
        allTasks = self.collection.aggregate([
            {
                '$match': {
                    'user_id': user_id,
                    'task_status': 'INACTIVE'
                }
            },
            {
                '$lookup': {
                    'from': 'categories',
                    'localField': 'category_id',
                    'foreignField': '_id',
                    'as': 'category'
                }
            }
        ])

        # Converter o cursor em uma lista
        allTasksList = list(allTasks)

        print("allTasks:")
        for task in allTasksList:
            print(task)

        tasks = []
        for task in allTasksList:
            category = task.get('category')
            task_viewmodel = {
                'task_id': str(task.get('_id')),
                'category': {
                    'category_id': str(category[0].get('_id')),
                    'category_name': category[0].get('category_name'),
                    'category_primary_color': category[0].get('category_primary_color'),
                    'category_secondary_color': category[0].get('category_secondary_color')
                },
                'task_name': task.get('task_name'),
                'task_date': task.get('task_date'),
                'task_hour': task.get('task_hour'),
                'task_description': task.get('task_description', None),
                'task_local': task.get('task_local', None),
                'task_status': task.get('task_status')
            }
            tasks.append(task_viewmodel)

        print(tasks)
        
        return tasks

    def update_task(self, task_id: str, category_id: str, task_name: Optional[str], task_date: Optional[date], task_hour: Optional[time], task_description: Optional[str], task_local: Optional[str], task_status: Optional[str]) -> Task:
        try:
            update_task = {}
            if task_name:
                update_task["task_name"] = task_name
            if task_date:
                update_task["task_date"] = task_date
            if task_hour:
                update_task["task_hour"] = task_hour
            if task_description:
                update_task["task_description"] = task_description
            if task_local:
                update_task["task_local"] = task_local
            if task_status:
                update_task["task_status"] = task_status
            if category_id:
                update_task["category_id"] = category_id

            self.collection.update_one({"_id": task_id}, {"$set": update_task})
            task = self.get_task_by_id(task_id)
            return task
        except Exception as e:
            print(f"Error: {e}")
            return ValueError(f"Error on update task, err: {e}")

    def delete_task_by_id(self, task_id: str) -> None:
        try:
            task = self.collection.find_one({"_id": task_id})
            if not task:
                return None
            self.collection.delete_one({"_id": task_id})
        except Exception as e:
            print(f"Error: {e}")
            return ValueError(f"Error on delete task by id, err: {e}")

    def get_task_by_day(self, task_date: date) -> List[Task]:
        tasks = []
        for task in self.collection.find({"task_date": task_date}):
            task_dto = TaskMongoDTO.from_mongo(task)
            task = task_dto.to_entity()
            tasks.append(task)
        return tasks
    