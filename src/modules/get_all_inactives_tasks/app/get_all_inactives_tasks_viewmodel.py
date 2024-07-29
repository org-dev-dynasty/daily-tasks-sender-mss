class GetAllInactivesTasksViewmodel:
    message: str

    def __init__(self, message: str):
        self.message = message

    def to_dict(self):
        return {
            "message": self.message
        }