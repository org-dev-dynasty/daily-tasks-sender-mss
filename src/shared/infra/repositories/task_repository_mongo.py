from pymongo import MongoClient
from src.shared.domain.entities.task import Task
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.infra.repositories.database.mongodb.task_collection import get_tasks_collection
from src.shared.infra.dto.task_mongo_dto import TaskMongoDTO

class TaskRepositoryMongo(ITaskRepository):
    tasks_collection: MongoClient

    def __init__(self, mongo_url: str):
        self.tasks_collection = get_tasks_collection(mongo_url)
    
    def create_task(self, task: Task) -> Task:
        try:
            task_dto = TaskMongoDTO.from_entity(task)
            task = TaskMongoDTO.to_entity(task_dto)

            self.tasks_collection.insert_one(TaskMongoDTO.to_mongo(TaskMongoDTO.from_entity(task)))
            return task
        except Exception as e:
            print(f'erro mongol repo: {e}')
            raise ValueError(f'Error creating task, erro: {e}')

    # def get_all_tasks(self) -> List[Task]:
    #     pass
