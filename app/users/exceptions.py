
class UserServiceError(Exception):
    """Base exception for all user-related service errors."""
    pass

class UsernameAlreadyTakenError(UserServiceError):
    pass 

class EmailAlreadyTakenError(UserServiceError):
    pass 

class InvalidCredentialsError(UserServiceError):
    pass 

class UserDoesNotExist(UserServiceError):
    pass

