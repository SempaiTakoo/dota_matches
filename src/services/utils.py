import re

from datetime import timedelta

import streamlit as st

from repositories.user import UserRepository


def get_username_by_user_id(user_id: int) -> str | None:
    user_repo = UserRepository()
    user = user_repo.get_user_by_id(user_id)

    if user:
        return user.username

    print(f'Пользователь с id {user_id} не найден')


def check_is_admin() -> bool:
    if st.session_state.user_role == 'admin':
        return True
    st.info('Только администратор может просматривать эту зону')
    return False


def convert_to_timedelta(duration_str: str) -> timedelta | None:
    '''Конвертирует строку формата `HH:mm:ss` в timedelta.'''
    match = re.match(r'(\d{2}):(\d{2}):(\d{2})', duration_str)

    if match:
        hours, minutes, seconds = map(int, match.groups())
        return timedelta(hours, minutes, seconds)

    st.error('Неверный формат. Используйте формат HH:mm:ss.')
