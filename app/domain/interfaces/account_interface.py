from abc import ABC, abstractmethod

from app.domain.models.account import Account, AccountId, NewAccount


class AccountInterface(ABC):
    @abstractmethod
    def add_one(self, new_account: NewAccount) -> Account | None:
        pass

    @abstractmethod
    def get_one(self) -> Account | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Account]:
        pass

    @abstractmethod
    def update_nickname(
        self, account_id: AccountId, new_nickname: str
    ) -> Account | None:
        pass

    @abstractmethod
    def update_rating(
        self, account_id: AccountId, rating_change: int
    ) -> Account | None:
        pass

    @abstractmethod
    def delete(self, account_id: AccountId) -> bool:
        pass
