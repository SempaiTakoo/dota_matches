from dataclasses import dataclass


@dataclass
class Account:
    id: int = None
    nickname: str = None
    rating: int = None
