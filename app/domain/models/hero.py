from dataclasses import dataclass
from typing import NewType


HeroId = NewType('HeroId', int)

@dataclass
class Hero:
    id: HeroId
    name: str
