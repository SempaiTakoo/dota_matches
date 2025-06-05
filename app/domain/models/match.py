from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import NewType


MatchId = NewType('MatchId', int)


@dataclass
class NewMatch:
    start_time: datetime
    duration: timedelta
    radiant_win: bool


@dataclass
class Match:
    id: MatchId
    start_time: datetime
    duration: timedelta
    radiant_win: bool
    radiant_kills: int
    dire_kills: int
