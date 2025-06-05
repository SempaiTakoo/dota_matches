from dataclasses import dataclass
from typing import NewType

from app.domain.models.player import PlayerId


ItemId = NewType('ItemId', int)


@dataclass
class Item:
    id: ItemId
    name: str


@dataclass
class PlayerItem:
    id: int
    player_id: PlayerId
    item_id: ItemId
