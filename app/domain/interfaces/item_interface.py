from abc import ABC, abstractmethod

from app.domain.models.item import Item, ItemId


class ItemInterface(ABC):
    @abstractmethod
    def add_one(self, new_item: Item) -> Item | None:
        pass

    @abstractmethod
    def get_one(self) -> Item | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Item]:
        pass

    @abstractmethod
    def update_name(self, item_id: ItemId) -> Item | None:
        pass

    @abstractmethod
    def delete(self, item_id: ItemId) -> bool:
        pass
