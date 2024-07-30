class UserAPIGatewayDTO:
    user_id: str
    username: str

    def __init__(self, user_id: str, username: str) -> None:
        self.user_id = user_id
        self.username = username

    @staticmethod
    def from_api_gateway(data: dict) -> "UserAPIGatewayDTO":
        return UserAPIGatewayDTO(
            user_id=data['sub'],
            username=data['cognito:username']
        )

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'username': self.username
        }
