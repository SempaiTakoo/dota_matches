from app.domain.interfaces.account_interface import AccountInterface
from app.domain.interfaces.auth_interface import AuthInterface, PasswordHasher, TokenStorageInterface
from app.domain.models.account import Account, NewAccount
from app.domain.models.auth_token import DEFAULT_TTL_SECONDS, AuthToken
from app.domain.models.user import NewUser, User, UserId
from app.domain.interfaces.user_interface import UserInterface


class AuthService(AuthInterface):
    def __init__(
        self,
        user_repository: UserInterface,
        account_repository: AccountInterface,
        token_storage_repository: TokenStorageInterface,
        password_hasher: PasswordHasher
    ) -> None:
        self.user_repository = user_repository
        self.account_repository = account_repository
        self.token_storage_repository = token_storage_repository
        self.password_hasher = password_hasher

    def register(self, new_user: NewUser, new_account: NewAccount) -> User | None:
        self.account_repository.add_one(new_account)
        return self.user_repository.add_one(new_user)

    def _is_correct_credentials(
        self, username: str, password: str, intended_user: User
    ) -> bool:
        return (username == intended_user.username
                and self.password_hasher.verify(password,
                                                intended_user.password_hash))

    def login(self, username: str, password: str) -> AuthToken | None:
        user = self.user_repository.get_by_username(username)

        if not user:
            return None

        if not self._is_correct_credentials(username, password, user):
            return None

        token = self.token_storage_repository.save_token(
            user_id=user.id, ttl_secods=DEFAULT_TTL_SECONDS
        )

        if not token:
            print(f'Не удалось сохранить token для {user.id=}.')
            return None

        return token

    def verify(self, user_id: UserId, intended_token: str) -> bool:
        token = self.token_storage_repository.get_token_by_user_id(user_id)

        if not token:
            print(f'Token для {user_id=} не найден.')

        return token == intended_token
