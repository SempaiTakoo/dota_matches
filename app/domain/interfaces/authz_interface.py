from abc import ABC, abstractmethod

from app.domain.models.user import User, UserId, UserRole


class AuthzInterface(ABC):
    @abstractmethod
    def has_role(self, user: User, role: UserRole) -> bool:
        pass
