from dataclasses import dataclass
from typing import NewType


AccountId = NewType('AccountId', int)


@dataclass
class NewAccount:
    nickname: str
    rating: int

@dataclass
class Account:
    id: AccountId
    nickname: str
    rating: int
