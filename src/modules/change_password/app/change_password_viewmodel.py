class ChangePasswordViewmodel:
    message: dict

    def __init__(self, message: dict):
        self.message = message
        
    def to_dict(self):
        return self.message