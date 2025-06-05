from abc import ABC, abstractmethod

from app.domain.models.player import NewPlayer, Player, PlayerId


class PlayerInterface(ABC):
    @abstractmethod
    def add_one(self, new_player: NewPlayer) -> Player | None:
        pass

    @abstractmethod
    def get_one(self, player_id: PlayerId) -> Player | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Player]:
        pass

    @abstractmethod
    def update_kda(
        self, kills_change: int, deaths_change: int, assistances_change: int
    ) -> Player | None:
        pass

    @abstractmethod
    def delete(self, player_id: PlayerId) -> bool:
        pass
