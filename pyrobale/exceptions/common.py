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





class TokenError(Exception):
    """Base class for token related errors"""
    pass


class InvalidClientError(TokenError):
    """Invalid authentication credentials"""
    pass


class BadRequestError(TokenError):
    """Invalid or incomplete parameters"""
    pass


class ServerError(TokenError):
    """Server related errors"""
    pass


class OTPError(Exception):
    """Base class for OTP related errors"""
    pass


class InvalidPhoneNumberError(OTPError):
    """Invalid phone number format"""
    pass


class UserNotFoundError(OTPError):
    """User not found"""
    pass


class InsufficientBalanceError(OTPError):
    """Insufficient balance"""
    pass


class RateLimitExceededError(OTPError):
    """Rate limit exceeded"""
    pass


class UnexpectedResponseError(OTPError):
    """Unexpected response from server"""
    pass
