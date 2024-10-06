class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class AttributeNotSpecifiedError(Exception):
    pass


class ServiceNotImplementedError(Exception):
    pass


class InvalidSignatureError(Exception):
    pass


class PaymentError(Exception):
    pass
