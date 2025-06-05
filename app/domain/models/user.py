from dataclasses import dataclass
from typing import NewType


UserId = NewType('UserId', int)


@dataclass
class NewUser:
    username: str
    password: str


@dataclass
class UserToCreate:
    username: str
    password_hash: str


@dataclass
class User:
    id: UserId
    username: str
    account_id: int
    role: str
    password_hash: str
