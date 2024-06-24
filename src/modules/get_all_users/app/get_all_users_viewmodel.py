from typing import List, Optional

from src.shared.domain.entities.user import User


class UserViewmodel:
    user_id: str
    name: str
    email: str
    phone: Optional[str]
    password: str

    def __init__(self, user_id: str, name: str, email: str, phone: Optional[str], password: str) -> None:
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "password": self.password
        }


class GetAllUsersViewmodel:
    users_viewmodel_list: List[UserViewmodel]

    def __init__(self, users: List[User]) -> None:
        users_list = []
        for user in users:
            user_viewmodel = UserViewmodel(
                user.user_id,
                user.name,
                user.email,
                user.phone,
                user.password
            )
            users_list.append(user_viewmodel)

        self.users_viewmodel_list = users_list
        print(self.users_viewmodel_list)

    def to_dict(self):
        users_list = []
        for user_viewmodel in self.users_viewmodel_list:
            user_viewmodel_to_dict = user_viewmodel.to_dict()
            users_list.append(user_viewmodel_to_dict)

        return {
            "users": users_list,
            "message": "All users have been retrieved successfully!"
        }
