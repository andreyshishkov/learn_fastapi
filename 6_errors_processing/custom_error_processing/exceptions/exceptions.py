from fastapi import HTTPException


class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, status_code=404):
        super().__init__(status_code=status_code, detail=detail)


class CustomExceptionB(HTTPException):
    def __init__(self, detail: str, status_code=403):
        super().__init__(status_code=status_code, detail=detail)