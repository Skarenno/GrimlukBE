class BFFException(Exception):
    pass

class MicroserviceUnavailableError(Exception):
    pass

class MicroserviceError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"[{status_code}] {detail}")
