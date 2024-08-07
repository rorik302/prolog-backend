from litestar.exceptions import HTTPException


class BaseAppException(Exception):
    def __init__(self, status_code: int | None = None, detail: str | None = None, default_detail: bool = False):
        self.detail = detail
        self.default_detail = default_detail
        self.status = status_code

    def raise_exception(self):
        if self.status is not None:
            detail = (
                self.detail
                if self.detail is not None and self.default_detail is False
                else self.__class__.__name__ if self.default_detail is False else None
            )
            raise HTTPException(detail=detail, status_code=self.status)
        raise NotImplementedError
