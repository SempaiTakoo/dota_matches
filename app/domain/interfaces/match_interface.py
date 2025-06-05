
from abc import ABC, abstractmethod

from app.domain.models.match import Match, MatchId, NewMatch


class MatchInterface(ABC):
    @abstractmethod
    def add_one(self, new_match: NewMatch) -> Match | None:
        pass

    @abstractmethod
    def get_one(self, match_id: MatchId) -> Match | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Match]:
        pass

    @abstractmethod
    def update_name(self, match_id: MatchId) -> Match | None:
        pass

    @abstractmethod
    def delete(self, match_id: MatchId) -> bool:
        pass
