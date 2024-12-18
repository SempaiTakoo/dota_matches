from dataclasses import dataclass


@dataclass
class User:
    id: int = None
    username: str = None
    account_id: int = None
    role: str = None
    password_hash: str = None
