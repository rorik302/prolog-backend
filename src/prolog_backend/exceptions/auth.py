from prolog_backend.exceptions.base import BaseAppException


class InvalidPassword(BaseAppException):
    pass


class InvalidAuthHeader(BaseAppException):
    pass


class InvalidToken(BaseAppException):
    pass


class SessionIDNotProvided(BaseAppException):
    pass


class InvalidSessionID(BaseAppException):
    pass
