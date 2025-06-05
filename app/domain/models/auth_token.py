from abc import ABC
from dataclasses import dataclass
from datetime import datetime

from app.domain.models.player import PlayerId


DEFAULT_TTL_SECONDS = 300


@dataclass
class AuthToken(ABC):
    user_id: PlayerId
    value: str
    expiration_time: datetime
