from prolog_backend.exceptions.base import BaseAppException


class UserDoesNotExist(BaseAppException):
    pass


class UserIsNotActive(BaseAppException):
    pass
