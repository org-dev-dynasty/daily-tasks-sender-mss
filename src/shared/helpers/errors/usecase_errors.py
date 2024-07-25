from src.shared.helpers.errors.base_error import BaseError


class NoItemsFound(BaseError):
    def __init__(self, message: str):
        super().__init__(f'No items found for {message}')


class DuplicatedItem(BaseError):
    def __init__(self, message: str):
        super().__init__(f'The item alredy exists for this {message}')


class ForbiddenAction(BaseError):
    def __init__(self, message: str):
        super().__init__(f'That action is forbidden for this {message}')


class InvalidCredentials(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Invalid credentials for {message}')


class TermsNotAccepted(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Terms not accepted for {message}')


class UserAlreadyConfirmed(BaseError):
    def __init__(self, message: str):
        super().__init__(f'The user is already confirmed for {message}')


class InvalidTokenError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'The token is invalid for {message}')


class UserNotConfirmed(BaseError):
    def __init__(self, message: str):
        super().__init__(f'The user is not confirmed for {message}')
