from typing import List

from src.shared.domain.entities.user import User


class LoginViewmodel:
    email: str
    password: str

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password": self.password
        }


class DoLoginViewmodel:
    users_viewmodel_list: LoginViewmodel

    def __init__(self, user: User) -> None:
        users_list = []
        user_viewmodel = LoginViewmodel(
            user.email,
            user.password,
        )
        users_list.append(user_viewmodel)

        self.users_viewmodel = user
        print(self.users_viewmodel)

    #  FIXME: Arrumar o método to_dict()
    def to_dict(self):
        users_list = []
        user_viewmodel_to_dict = self.users_viewmodel
        users_list.append(user_viewmodel_to_dict)

        return {
            "user": users_list,
            "message": "User logged!"
        }
