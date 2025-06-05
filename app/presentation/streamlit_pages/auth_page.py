from app.domain.interfaces.account_interface import AccountInterface
from app.domain.interfaces.auth_interface import AuthInterface
from app.domain.interfaces.user_interface import UserInterface
from app.domain.models.account import NewAccount
from app.domain.models.user import NewUser
import streamlit as st

from app.presentation.streamlit_pages.session_states import PageState


def registration_page(
    auth_service: AuthInterface,
    account_service: AccountInterface
):
    username = st.text_input('Имя пользователя')
    password = st.text_input('Пароль', type='password')
    password_again = st.text_input('Подтвердите пароль', type='password')

    nickname = st.text_input('Игровой псевдоним (никнейм)')
    rating = st.number_input('Ваш текущий рейтинг')

    if st.button('Зарегистрироваться'):
        if password != password_again:
            st.error('Пароли не совпадают')
            return

        if rating < 0:
            st.error('Рейтинг не может быть отрицательным')
            return

        new_user = NewUser(username=username, password=password)
        new_account = NewAccount(nickname=nickname, rating=rating)
        try:
            auth_service.register(new_user)
            account_service.add_one(new_account)
            st.success(
                'Пользователь и игровой аккаунт успешно зарегистрированы!'
            )
            st.session_state.page = PageState.AUTH
            st.rerun()

        except Exception as e:
            st.error(str(e))
            return


def login_page(user_service: UserInterface, auth_service: AuthInterface):
    username = st.text_input('Имя пользователя')
    password = st.text_input('Пароль', type='password')

    if st.button('Войти'):
        user = user_service.get_by_username(username)

        if not user:
            st.error('Пользователь не найден')
            return

        token = auth_service.login(username, password)

        if token:
            st.session_state.token = token
            st.session_state.user_id = user.id
            st.session_state.page = PageState.PROFILE
            st.success('Успешный вход в систему!')
            st.rerun()
        else:
            st.error('Неверные данные пользователя')
            return
