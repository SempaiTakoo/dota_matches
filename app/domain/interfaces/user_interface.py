from abc import ABC, abstractmethod

from app.domain.models.user import NewUser, User, UserId


class UserInterface(ABC):
    @abstractmethod
    def add_one(self, new_user: NewUser) -> User | None:
        pass

    @abstractmethod
    def get_one(self, user_id: UserId) -> User | None:
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def get_by_username(self, username) -> User | None:
        pass

    @abstractmethod
    def update_username(self, user_id: UserId, new_username: str) -> User | None:
        pass

    @abstractmethod
    def delete(self, user_id: UserId) -> bool:
        pass
