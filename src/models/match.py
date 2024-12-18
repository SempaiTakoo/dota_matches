from datetime import datetime, timedelta

from dataclasses import dataclass


@dataclass
class Match:
    id: int = None
    start_time: datetime = None
    duration: timedelta = None
    radiant_win: bool = None
    radiant_kills: int = None
    dire_kills: int = None
