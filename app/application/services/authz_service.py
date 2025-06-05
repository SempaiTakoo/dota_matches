from app.domain.interfaces.authz_interface import AuthzInterface
from app.domain.interfaces.user_interface import UserInterface
from app.domain.models.user import User, UserRole


class AuthzService(AuthzInterface):
    def __init__(self, user_repository: UserInterface) -> None:
        self.user_repository = user_repository

    def has_role(self, user: User, role: UserRole) -> bool:
        return user.role == role
