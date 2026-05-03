class OTPResult:
    """Container for OTP result with code and response data"""

    def __init__(self, code: int, response: dict):
        self.code = code
        self.response = response

    def __repr__(self):
        return f"OTPResult(code={self.code}, response={self.response})"
