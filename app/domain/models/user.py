from dataclasses import dataclass
import enum
from typing import NewType


UserId = NewType('UserId', int)


class UserRole(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'


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
    role: UserRole
    password_hash: str
