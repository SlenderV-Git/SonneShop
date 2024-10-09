from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(detail=message, status_code=status.HTTP_404_NOT_FOUND)


class ConflictError(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_409_CONFLICT)


class AttributeNotSpecifiedError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            detail=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class ServiceNotImplementedError(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_501_NOT_IMPLEMENTED)


class InvalidSignatureError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            detail=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class PaymentError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            detail=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class WarehouseError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class AccountError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)
