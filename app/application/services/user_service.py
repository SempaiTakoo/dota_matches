from app.domain.interfaces.user_interface import UserInterface
from app.domain.models.user import NewUser, User, UserId
from services.auth import AuthService


class UserService:
    def __init__(self, user_repository: UserInterface) -> None:
        self.user_repository = user_repository
        self.auth_service

    def get_user(self, user_id: UserId) -> User | None:
        self.user_repository.get_one(user_id)

    def get_users(self, )
