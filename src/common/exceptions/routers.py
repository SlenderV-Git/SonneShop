from fastapi import HTTPException, status


class CustomException(HTTPException):
    def __init__(self, message: str, status_code: int):
        self.message = message
        super().__init__(detail=message, status_code=status_code)

    def __str__(self):
        return self.message

    def get_dict(self) -> dict:
        return self.__dict__


class UnAuthorizedException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ConflictException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_409_CONFLICT)


class NotFoundException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_404_NOT_FOUND)
