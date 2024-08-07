import hashlib
from enum import Enum

from argon2 import PasswordHasher


class Algorithm(str, Enum):
    ARGON2 = "ARGON2"
    SHA1 = "SHA1"


class Hasher:
    @classmethod
    def hash(cls, value: str, algorithm: Algorithm = Algorithm.ARGON2) -> str:
        if algorithm == Algorithm.ARGON2:
            return PasswordHasher().hash(value)
        if algorithm == Algorithm.SHA1:
            return hashlib.sha1(string=value.encode("utf-8")).hexdigest()

    @classmethod
    def verify(cls, hashed: str, password: str) -> bool:
        return PasswordHasher().verify(hash=hashed, password=password)
