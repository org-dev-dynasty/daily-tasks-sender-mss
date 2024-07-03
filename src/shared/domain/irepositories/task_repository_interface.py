from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.task import Task


class ITaskRepository(ABC):
  @abstractmethod
  def get_all_users(self) -> List[Task]:
    pass
  
  @abstractmethod
  def create_user(self, task: Task) -> Task:
    pass
