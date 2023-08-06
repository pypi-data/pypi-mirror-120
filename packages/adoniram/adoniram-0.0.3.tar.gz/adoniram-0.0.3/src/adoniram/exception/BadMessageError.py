class BadMessageError(Exception):
    def __init__(self, message: str, raw: bytes):
        super().__init__(message)
        self.raw = raw
