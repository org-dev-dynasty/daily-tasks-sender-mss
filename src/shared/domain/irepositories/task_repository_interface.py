from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.task import Task


class ITaskRepository(ABC):
  @abstractmethod
  def get_all_tasks(self) -> List[Task]:
    pass
  
  @abstractmethod
  def create_task(self, task: Task) -> Task:
    pass
