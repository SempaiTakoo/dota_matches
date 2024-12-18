from passlib.hash import bcrypt

from models.user import User
from repositories.user import UserRepository
from repositories.account import AccountRepository


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.account_repo = AccountRepository()

    def register(
        self, nickname: str, rating: int, username: str, password: str
    ):
        role = 'user'

        if username == 'admin':
            role = 'admin'

        if self.user_repo.get_user_by_username(username):
            raise ValueError('Пользователь с таким username уже существует')

        new_account_id = self.account_repo.add_account(
            nickname=nickname,
            rating=rating
        )

        password_hash = bcrypt.hash(password)

        user = User(
            username=username,
            account_id=new_account_id,
            password_hash=password_hash,
            role=role
        )

        self.user_repo.add_user(user)
        print(f'Пользователь {user.username} зарегистрирован')

    def authenticate(self, username: str, password: str):
        user = self.user_repo.get_user_by_username(username)

        if user and bcrypt.verify(password, user.password_hash):
            return user
