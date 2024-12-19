import streamlit as st

from services.utils import check_is_admin, get_username_by_user_id

from views.auth import AuthView
from views.user import UserView
from views.item import ItemView
from views.hero import HeroView
from views.match import MatchView
from views.player import PlayerView

SESSION_STATE_PARAMS = ('user_role', 'user_id', 'page')


def init_session_state_params(params: tuple[str]) -> None:
    for key in params:
        if key not in st.session_state:
            st.session_state[key] = None


def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)


def show_navigation_radio(
    authorized: list[str], unauthorized: list[str]
) -> None:
    if st.session_state.user_id:
        username = get_username_by_user_id(st.session_state.user_id)
        st.session_state.page = st.sidebar.radio(
            f'Добро пожаловать, {username}!', authorized
        )
    else:
        st.session_state.page = st.sidebar.radio('Войдите в систему', unauthorized)


def show_entry_page() -> None:
    st.title('Статистика Dota 2')
    st.header('Навигация')

    authorized_pages = [
        'Мой профиль', 'Выйти', 'Герои', 'Предметы', 'Матчи', 'Аккаунты'
    ]
    unauthorized_pages = ['Авторизация', 'Регистрация']

    if st.session_state.user_role == 'admin':
        authorized_pages += ['Участники матчей', 'Пользователи']

    show_navigation_radio(authorized_pages, unauthorized_pages)

    auth_view = AuthView()
    user_view = UserView()
    item_view = ItemView()
    hero_view = HeroView()
    match_view = MatchView()
    player_view = PlayerView()

    pages = {
        'Авторизация': auth_view.show_login,
        'Регистрация': auth_view.show_register,

        'Мой профиль': user_view.show_profile,
        'Выйти': auth_view.show_logout,
        'Аккаунты': user_view.show_accounts,
        'Герои': hero_view.show_heroes,
        'Предметы': item_view.show_items,
        'Матчи': match_view.show_matches,

        'Пользователи': user_view.show_user_list,
        'Участники матчей': player_view.show_player_list,
    }
    print(f'Page: {st.session_state.page}')
    pages[st.session_state.page]()


if __name__ == '__main__':
    init_session_state_params(SESSION_STATE_PARAMS)
    # hide_sidebar()
    show_entry_page()
