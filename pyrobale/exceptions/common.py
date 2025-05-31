class PyroBaleException(Exception):
    pass


class InvalidTokenException(PyroBaleException):
    pass


class NotFoundException(PyroBaleException):
    pass

class ForbiddenException(PyroBaleException):
    pass

class InternalServerException(PyroBaleException):
    pass