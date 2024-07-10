from src.shared.domain.entities.task import Task
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.infra.repositories.database.mongodb.task_collection import get_tasks_collection
from typing import List

''' 
NAO SEI SE ESTA CORRETO O REPO APENAS TESTANDO, digao 10/07/24
'''


class TaskRepositoryMongo(ITaskRepository):
    def __init__(self, mongo_url: str):
        self.users_collection = get_tasks_collection(mongo_url)

    def create(self, task: Task) -> Task:
        self.collection.insert_one(task.dict())
        return task

    def get(self, task_id: str) -> Task:
        task = self.collection.find_one({"task_id": task_id})
        return Task(**task)

    def list(self) -> List[Task]:
        tasks = self.collection.find()
        return [Task(**task) for task in tasks]

    def update(self, task: Task) -> Task:
        self.collection.update_one({"task_id": task.task_id}, {"$set": task.dict()})
        return task

    def delete(self, task_id: str) -> None:
        self.collection.delete_one({"task_id": task_id})