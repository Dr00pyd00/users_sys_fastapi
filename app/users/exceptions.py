
class UserServiceError(Exception):
    """Base exception for all user-related service errors."""
    pass

# User ------------------------------------------------
class UsernameAlreadyTakenError(UserServiceError):
    pass 

class EmailAlreadyTakenError(UserServiceError):
    pass 

class InvalidCredentialsError(UserServiceError):
    pass 

class UserDoesNotExist(UserServiceError):
    pass

# Tokens JWT ------------------------------------------
class InvalidRefreshToken(UserServiceError):
    pass

