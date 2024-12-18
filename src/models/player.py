from dataclasses import dataclass


@dataclass
class Player:
    id: int = None
    account_id: int = None
    match_id: int = None
    hero_id: int = None
    kills: int = None
    deaths: int = None
    assistances: int = None
    is_radiant: bool = None
    rating_change: int = None
