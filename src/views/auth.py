import streamlit as st

from services.auth import AuthService


class AuthView:
    def __init__(self) -> None:
        self.auth_service = AuthService()

    def show_register(self) -> None:
        st.header('Регистрация')

        nickname = st.text_input('Никнейм')
        rating = st.number_input('Текущий рейтинг')

        username = st.text_input('Логин')
        password = st.text_input('Пароль', type='password')
        password_again = st.text_input('Подтвердите парль', type='password')

        if st.button('Зарегистрироваться'):

            if password != password_again:
                st.error('Пароли не совпадают')
                return

            try:
                self.auth_service.register(
                    nickname=nickname,
                    rating=rating,
                    username=username,
                    password=password
                )
                st.success('Пользователь успешно зарегистрирован')

            except Exception as e:
                st.error(str(e))

    def show_login(self):
        st.header('Авторизация')

        username = st.text_input('Логин')
        password = st.text_input('Пароль', type='password')

        if st.button('Войти'):
            user = self.auth_service.authenticate(username, password)

            if user:
                st.info(f'Добро пожаловать, {user.username}!')
                role = user.role
                st.session_state.user_role = role
                st.session_state.user_id = user.id
                st.session_state.page = 'Мой профиль'
                st.rerun()
            else:
                st.error('Неверный логин или пароль')

    def show_logout(self):
        st.header('Выйти из аккаунта')

        if st.button('Выйти'):
            st.session_state.user_role = 'user'
            st.session_state.user_id = None
            st.session_state.page = 'Регистрация'
            st.rerun()
