class UserViewmodel:
    access_token: str
    id_token: str
    user_id: str

    def __init__(self, access_token: str, id_token: str,  user_id: str = None, **kwargs):
        self.access_token = access_token
        self.id_token = id_token
        self.user_id = user_id

    def to_dict(self):
        return {
            'access_token': self.access_token,
            'id_token': self.id_token,
            'user_id': self.user_id,
        }


class LoginViewmodel:
    user: UserViewmodel

    def __init__(self, data: dict):
        self.user = UserViewmodel(**data)

    def to_dict(self):
        return {
            'token': self.user.access_token,
            'user': self.user.to_dict(),
            'message': 'Login successful'
        }
