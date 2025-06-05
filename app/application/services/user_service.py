from app.application.services.auth_service import AuthService
from app.application.services.authz_service import AuthzService
from app.domain.interfaces.user_interface import UserInterface
from app.domain.models.user import User, UserId


class UserService:
    def __init__(
        self,
        user_repository: UserInterface,
        auth_service: AuthService,
        authz_service: AuthzService
    ) -> None:
        self.user_repository = user_repository
        self.auth_service = auth_service
        self.authz_service = authz_service
