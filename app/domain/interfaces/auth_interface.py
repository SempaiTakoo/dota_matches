from abc import ABC, abstractmethod

from app.domain.models.auth_token import AuthToken
from app.domain.models.user import NewUser, User, UserId


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        pass


class TokenStorageInterface(ABC):
    @abstractmethod
    def save_token(self, user_id: UserId, ttl_secods: int) -> AuthToken | None:
        pass

    @abstractmethod
    def get_token_by_user_id(self, user_id: UserId) -> AuthToken | None:
        pass

    @abstractmethod
    def delete_token(self, token: str) -> bool:
        pass


class AuthInterface(ABC):
    @abstractmethod
    def register(self, new_user: NewUser) -> User | None:
        pass

    @abstractmethod
    def login(self, username: str, password: str, ) -> AuthToken | None:
        pass

    @abstractmethod
    def verify(self, user_id: UserId, intended_token: str) -> bool:
        pass
