import logging
from typing import List

from pymongo import MongoClient
from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.infra.dto.user_mongo_dto import UserMongoDTO
from src.shared.infra.repositories.database.mongodb.user_collection import get_users_collection


class UserRepositoryMongo(IUserRepository):
    users_collection: MongoClient

    def __init__(self, mongo_url: str):
        self.users_collection = get_users_collection(mongo_url)

    def create_user(self, name: str, email: str, phone: str, password: str) -> User:
        user_dto = UserMongoDTO(name=name, email=email, phone=phone, password=password)
        user = UserMongoDTO.to_entity(UserMongoDTO.from_mongo(user_dto))
        self.users_collection.insert_one(UserMongoDTO.to_mongo(UserMongoDTO.from_entity(user)))
        logging.info(f'User created [Create] - {user}')
        return user

    def get_all_users(self) -> List[User]:
        try:
            users = self.users_collection.find()
            logging.info(f'All_users [Get-All] - {users}')
            return [UserMongoDTO.to_entity(UserMongoDTO.from_mongo(user)) for user in users]
        except Exception as e:
            logging.error('Error getting all users')
            raise ValueError(f'Error getting all users, erro: {e}')


def get_user_by_id(self, user_id: str) -> User:
    user = self.users_collection.find_one({"_id": user_id})
    return user


def login(self, email: str, password: str) -> User:
    user = self.users_collection.find_one({"email": email, "password": password})
    return user
