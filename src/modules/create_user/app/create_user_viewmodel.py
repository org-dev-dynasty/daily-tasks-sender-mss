from src.shared.domain.entities.user import User


class UserViewmodel:
    name: str
    email: str

    def __init__(self, data, verification_code=None):
        if verification_code is not None:
            self.user_id = data['user']["user_id"]
            self.name = data['user']["name"]
            self.email = data['user']["email"]
            self.verification_code = data["verification_code"]
        else:
            self.user_id = data.user_id
            self.name = data.name
            self.email = data.email
        

    def to_dict(self):
        if hasattr(self, 'verification_code'):
            return {
                'user_id': self.user_id,
                'name': self.name,
                'email': self.email,
                'verification_code': self.verification_code
            }
        
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            
        }


class CreateUserViewmodel:
    user: UserViewmodel

    def __init__(self, user: User, verification_code=None):
        if verification_code is None:
            self.user = UserViewmodel(user)
        else:
            self.user = UserViewmodel(user, verification_code)
            

    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'message': 'the user was created'
        }
