
class AuthServiceError(Exception):
    pass 

# Tokens JWT ------------------------------------------
class InvalidRefreshToken(AuthServiceError):
    pass

class InvalidCredentialsError(AuthServiceError):
    pass 


