from dataclasses import dataclass
from typing import NewType


PlayerId = NewType('PlayerId', int)


@dataclass
class NewPlayer:
    account_id: int
    match_id: int
    hero_id: int
    kills: int
    deaths: int
    assistances: int
    is_radiant: bool
    rating_change: int


@dataclass
class Player:
    id: PlayerId
    account_id: int
    match_id: int
    hero_id: int
    kills: int
    deaths: int
    assistances: int
    is_radiant: bool
    rating_change: int
