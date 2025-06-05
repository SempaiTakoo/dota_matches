from abc import ABC, abstractmethod

from app.domain.models.hero import Hero, HeroId


class HeroInterface(ABC):
    @abstractmethod
    def add_one(self, new_hero: Hero) -> Hero | None:
        pass

    @abstractmethod
    def get_one(self) -> Hero | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Hero]:
        pass

    @abstractmethod
    def update_name(self, hero_id: HeroId) -> Hero | None:
        pass

    @abstractmethod
    def delete(self, hero_id: HeroId) -> bool:
        pass
