from src.shared.domain.entities.user import User


class UserViewmodel:
    name: str
    email: str

    def __init__(self, user: User):
        self.user_id = user.cognito_id
        self.name = user.name
        self.email = user.email

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
        }


class CreateUserViewmodel:
    user: UserViewmodel

    def __init__(self, user: User):
        self.user = UserViewmodel(user)

    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'message': 'the user was created'
        }
