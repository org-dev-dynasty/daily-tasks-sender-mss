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
        usersList = []
        try:
            print('OLAAAAAAAAA REPO MONGOLLLL')
            users = self.users_collection.find()
            print(f'users_find: {users}')
            print(f'type_users: {type(users)}')
            print(f'user mongol')

            for user in users:
                try:
                    print(f'Validando usuário: {user}')
                    if not all(key in user for key in ["name", "email", "password"]):
                        print(f'Usuário inválido: {user}')
                except Exception as e:
                    print(f'Erro ao validar usuário: {e}')
            
            for user in users:
                try:
                    print(f'user: {user}')
                    user_dto = UserMongoDTO.from_mongo(user)
                    print(f'user_dto: {user_dto}')
                    user_entity = user_dto.to_entity()
                    print(f'user_entity: {user_entity}')
                    usersList.append(user_entity)

                except Exception as inner_e:
                    print(f'Erro processando usuário {user}: {inner_e}')
                
            return usersList

        except Exception as e:
            print(f'erro mongol repo: {e}')
            raise ValueError(f'Error getting all users, erro: {e}')


def get_user_by_id(self, user_id: str) -> User:
    user = self.users_collection.find_one({"_id": user_id})
    return user


def login(self, email: str, password: str) -> User:
    user = self.users_collection.find_one({"email": email, "password": password})
    return user
