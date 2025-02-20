from typing import Optional

from src.shared.domain.entities.user import User


class UserMongoDTO:
    user_id: Optional[str]
    name: str
    email: str
    phone: Optional[str]
    password: str

    def __init__(self, user_id: Optional[str], name: str, email: str, phone: Optional[str], password: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password

    @staticmethod
    def from_mongo(data) -> "UserMongoDTO":
        try:
            print(f'data vinda do mongo: {data}')
            obj_id = data["_id"]
            print(f"obj_id AQUIIII: {obj_id}")
            user_id = str(obj_id)

            return UserMongoDTO(
                user_id=user_id,
                name=data["name"],
                email=data["email"],
                phone=data.get("phone"),
                password=data["password"]
            )
        except KeyError as e:
            print(f'KeyError: {e} em data: {data}')
            raise

    # @staticmethod
    def to_entity(self) -> User:
        print('OI TO ENTITY')
        return User(
            user_id=self.user_id,
            name=self.name,
            email=self.email,
            phone=self.phone,
            password=self.password
        )

    @classmethod
    def to_mongo(cls, user: User):
        return {
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "password": user.password
        }

    def from_entity(user: User) -> "UserMongoDTO":
        return UserMongoDTO(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            password=user.password
        )
