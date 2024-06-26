from typing import List

from pymongo import MongoClient
from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.infra.repositories.database.mongodb.user_collection import get_users_collection

class UserRepositoryMongo(IUserRepository):
  users_collection: MongoClient
  
  def __init__(self, mongo_url: str):
    self.users_collection = get_users_collection(mongo_url)
  
  def get_all_users(self) -> List[User]:
    users = self.users_collection.find()
    
    
    
    
    