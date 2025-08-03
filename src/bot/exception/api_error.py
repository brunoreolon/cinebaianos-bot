class ApiError(Exception):
    def __init__(self, code, message, status):
        self.code = code
        self.message = message
        self.status = status
        super().__init__(message)
