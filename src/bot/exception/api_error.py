class ApiError(Exception):
    def __init__(self, code, title, detail, status, options=None):
        self.code = code
        self.title = title
        self.detail = detail
        self.status = status
        self.options = options
        super().__init__(detail)