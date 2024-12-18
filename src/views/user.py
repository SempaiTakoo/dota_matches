import streamlit as st

import pandas as pd

from services.utils import check_is_admin

from repositories.account import AccountRepository
from repositories.user import UserRepository


class UserView:
    def __init__(self) -> None:
        self.user_repo = UserRepository()
        self.account_repo = AccountRepository()

    def show_user_list(self) -> None:
        st.header('Список всех пользователей')

        if not check_is_admin():
            return

        users = self.user_repo.get_all_users()
        data = pd.DataFrame(
            [
                {
                    'ID': user.id,
                    'Имя пользователя': user.username,
                    'Роль': user.role,
                    'ID Аккаунта': user.account_id
                }
                for user in users
            ]
        )
        st.dataframe(data, hide_index=True)

        user_ids = [user.id for user in users]
        selected_id = st.selectbox(
            'Выберите ID пользователя для изменения или удаления', user_ids
        )

        if selected_id:
            self.show_user_detail(selected_id)

    def show_user_detail(self, selected_id) -> None:
        selected_user = self.user_repo.get_user_by_id(selected_id)

        if not selected_user:
            st.error(f'Пользователь с ID {selected_id} не найден')

        st.subheader(f'Выбран пользователь: {selected_user.username}')

        new_username = st.text_input(
            'Новое имя пользователя', selected_user.username
        )
        new_role = st.text_input(
            'Новая роль пользователя', selected_user.role
        )

        if st.button('Обновить пользователя'):
            if new_username.strip() and new_role.strip():
                try:
                    self.user_repo.update_user(
                        selected_user.id, new_username.strip(), new_role.strip()
                    )
                    st.success('Пользователь успешно обновлён!')
                except Exception as e:
                    st.error(
                        f'Произошла ошибка при обновлении пользователя: {e}'
                    )
            else:
                st.warning('Имя пользователя и роль не могут быть пустыми!')

        if st.button('Удалить пользователя'):
            try:
                account_id = selected_user.account_id
                self.user_repo.delete_user(selected_user.id)
                self.account_repo.delete_account(account_id)
                st.success('Пользователь успешно удалён!')

            except Exception as e:
                st.error(f'Произошла ошибка при удалении пользователя: {e}')

    def show_profile(self) -> None:
        st.header('Мой профиль')

        user_id = st.session_state.get('user_id')

        if not user_id:
            st.warning('Пожалуйста, авторизуйтесь, чтобы просмотреть профиль.')
            return

        user = self.user_repo.get_user_by_id(user_id)

        if not user:
            st.error('Пользователь не найден.')
            return

        account = self.account_repo.get_account_by_id(user.account_id)

        if not account:
            st.error('Аккаунт не найден.')
            return

        st.write(f'Имя пользователя: {user.username}')
        st.write(f'Роль: {user.role}')
        st.write(f'Никнейм: {account.nickname}')
        st.write(f'Рейтинг: {account.rating}')

    def show_accounts(self):
        st.header('Аккаунты')

        accounts = self.account_repo.get_all_accounts()

        if accounts:
            data = pd.DataFrame(
                [
                    {
                        'Никнейм': account.nickname,
                        'Рейтинг': account.rating
                    }
                    for account in accounts
                ]
            )
            st.dataframe(data, use_container_width=True, hide_index=True)
        else:
            st.info('Аккаунты не найдены.')
