from src.shared.domain.entities.task import Task
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.infra.dto.task_mongo_dto import TaskMongoDTO
from src.shared.infra.repositories.database.mongodb.task_collection import get_tasks_collection
from typing import List, Optional
from datetime import date, time


class TaskRepositoryMongo(ITaskRepository):

    def __init__(self, mongo_url: str):
        self.collection = get_tasks_collection(mongo_url)

    def create_task(self, task: Task) -> Task:
        self.collection.insert_one(task.to_dict())
        return task

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        try:
            task = self.collection.find_one({"_id": task_id})
            if not task:
                return None
            task_dto = TaskMongoDTO.from_mongo(task)
            task = task_dto.to_entity()
            return task
        except Exception as e:
            print(f"Error: {e}")
            return ValueError(f"Error on get task by id, err: {e}")

    def get_all_tasks(self) -> List[Task]:
        tasks = []
        for task in self.collection.find():
            task_dto = TaskMongoDTO.from_mongo(task)
            task = task_dto.to_entity()
            tasks.append(task)
        return tasks

    def update_task(self, task_id: str, task_name: Optional[str], task_date: Optional[date], task_hour: Optional[time], task_description: Optional[str], task_local: Optional[str], task_status: Optional[str]) -> Task:
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

    def update_task_status(self, task_id: str, task_status: str) -> Task:
        try:
            self.collection.update_one({"_id": task_id}, {"$set": {"task_status": task_status}})
            task = self.get_task_by_id(task_id)
            print(task)
            return task
        except Exception as e:
            print(f"Error: {e}")
            return ValueError(f"Error on update task status, err: {e}")
