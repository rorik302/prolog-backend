from argon2 import PasswordHasher


class Hasher:
    @classmethod
    def hash(cls, value: str) -> str:
        return PasswordHasher().hash(value)
