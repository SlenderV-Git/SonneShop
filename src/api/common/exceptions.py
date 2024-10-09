from fastapi import HTTPException, status


class CommandNotFoundError(Exception):
    pass


class ForbiddenError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status.HTTP_403_FORBIDDEN, detail)
