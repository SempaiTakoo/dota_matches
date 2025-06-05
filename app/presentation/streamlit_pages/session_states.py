import enum
import streamlit as st


class PageState(enum.Enum):
    AUTH = 'Авторизация'
    REGISTRATION = 'Регистрация'
    PROFILE = 'Мой профиль'
    HEROES = 'Герои'
    ITEMS = 'Предметы'
    ACCOUNTS = 'Аккаунты'
    MATCHES = 'Матчи'
