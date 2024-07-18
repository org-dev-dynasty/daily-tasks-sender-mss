from src.shared.domain.entities.task import Task
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.infra.dto.task_mongo_dto import TaskMongoDTO
from src.shared.infra.repositories.database.mongodb.task_collection import get_tasks_collection
from typing import List, Optional


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