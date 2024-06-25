from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
import logging

from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.infra.repositories.database.models import Base, UserModel
from src.shared.infra.dto.user_postgres_dto import UserPostgresDTO  

class UserRepositoryPostgres(IUserRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, pool_size=10, max_overflow=20)
        Base.metadata.create_all(bind=self.engine)
        self.Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    def create_user(self, user_props: User) -> User:
        session = self.Session()
        try:
            existing_user = session.query(UserModel).filter_by(email=user_props.email).first()

            if existing_user:
                raise ValueError("User already exists in the database.")

            new_user = UserModel(
                user_id=uuid4(),
                name=user_props.name,
                email=user_props.email,
                phone=user_props.phone,
                password=user_props.password
            )

            session.add(new_user)
            session.commit()

            return User(
                user_id=new_user.user_id,
                name=new_user.name,
                email=new_user.email,
                phone=new_user.phone,
                password=new_user.password
            )

        except IntegrityError as e:
            session.rollback()
            raise ValueError("Erro ao criar usuário no banco de dados: " + str(e))
        
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao criar usuário: " + str(e))
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        session = self.Session()
        try:
            existing_user = session.query(UserModel).filter_by(email=email).first()

            if not existing_user:
                return None

            return User(
                user_id=existing_user.id,
                name=existing_user.name,
                email=existing_user.email,
                phone=existing_user.telefone,
                password=existing_user.password,
            )

        except Exception as e:
            logging.error(f"Erro ao buscar usuário por email: {e}")
            raise ValueError("Erro ao buscar usuário por email")

    def get_all_users(self) -> List[User]:
        session = self.Session()
        try:
            all_users = session.query(UserModel).all()
            logging.info(f'All_users [Get-All] - {all_users}')
            return [UserPostgresDTO.to_entity(UserPostgresDTO.from_postgres(user)) for user in all_users]

        except Exception as e:
            logging.error(f"Erro ao buscar todos os usuários: {e}")
            raise ValueError("Erro ao buscar todos os usuários")
    

    # def get_user_by_id(self, user_id: str) -> Optional[User]:
    #     try:
    #         existing_user = self.session.query(UserModel).filter_by(id=user_id).first()

    #         if not existing_user:
    #             return None

    #         return User(
    #             user_id=existing_user.user_id,
    #             name=existing_user.name,
    #             email=existing_user.email,
    #             phone=existing_user.phone,
    #             password=existing_user.password,
    #             phone=existing_user.phone,
    #         )

    #     except Exception as e:
    #         print(f"Erro ao buscar usuário por ID: {e}")
    #         raise ValueError("Erro ao buscar usuário por ID")




