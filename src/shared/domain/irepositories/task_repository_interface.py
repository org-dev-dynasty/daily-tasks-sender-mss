from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date, time

from src.shared.domain.entities.task import Task


class ITaskRepository(ABC):
  @abstractmethod
  def get_all_tasks(self, user_id: str) -> List[Task]:
    pass
  
  @abstractmethod
  def create_task(self, task: Task) -> Task:
    pass
  
  @abstractmethod
  def get_task_by_id(self, task_id: str) -> Task:
    pass

  def update_task(self, task_id: str, category_id: str, task_name: Optional[str], task_date: Optional[date], task_hour: Optional[time], task_description: Optional[str], task_local: Optional[str], task_status: Optional[str]) -> Task:
    pass
  
  def delete_task_by_id(self, task_id: str) -> None:
    pass

  def get_task_by_day(self, task_date: date) -> List[Task]:
    pass