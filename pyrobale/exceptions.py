class BaleException(Exception):
    """Base exception for Bale API errors"""

    def __init__(self, message=None, error_code=None, response=None):
        self.message = message
        self.error_code = error_code
        self.response = response

        error_text = f"Error {error_code}: {message}" if error_code and message else message or str(
            error_code)
        super().__init__(error_text)

    def __str__(self):
        error_details = []
        if self.error_code:
            error_details.append(f"code={self.error_code}")
        if self.message:
            error_details.append(f"message='{self.message}'")
        details = ", ".join(error_details)
        return f"{self.__class__.__name__}({details})"


class BaleAPIError(BaleException):
    """Exception raised when Bale API returns an error response"""
    pass


class BaleNetworkError(BaleException):
    """Exception raised when network-related issues occur during API calls"""
    pass


class BaleAuthError(BaleException):
    """Exception raised when authentication fails or token is invalid"""
    pass


class BaleValidationError(BaleException):
    """Exception raised when request data fails validation"""
    pass


class BaleTimeoutError(BaleException):
    """Exception raised when API request times out"""
    pass


class BaleNotFoundError(BaleException):
    """Exception raised when requested resource is not found (404)"""
    pass


class BaleForbiddenError(BaleException):
    """Exception raised when access to resource is forbidden (403)"""
    pass


class BaleServerError(BaleException):
    """Exception raised when server encounters an error (5xx)"""
    pass


class BaleRateLimitError(BaleException):
    """Exception raised when API rate limit is exceeded (429)"""
    pass


class BaleTokenNotFoundError(BaleException):
    """Exception raised when required API token is missing"""
    pass


class BaleUnknownError(BaleException):
    """Exception raised for unexpected or unknown errors"""
    pass
