import streamlit as st

import pandas as pd

from datetime import datetime, time

from models.match import Match

from repositories.account import AccountRepository
from repositories.hero import HeroRepository
from repositories.item import ItemRepository
from repositories.match import MatchRepository
from repositories.player import PlayerRepository
from repositories.player_items import PlayerItemsRepository
from services.utils import check_is_admin, convert_to_timedelta


class MatchView:
    def __init__(self) -> None:
        self.match_repo = MatchRepository()
        self.player_repo = PlayerRepository()
        self.account_repo = AccountRepository()
        self.hero_repo = HeroRepository()
        self.player_items_repo = PlayerItemsRepository()
        self.item_repo = ItemRepository()

    def show_matches(self) -> None:
        st.header('Список матчей')

        matches = self.match_repo.get_all_matches()
        players = self.player_repo.get_all_players()
        accounts = self.account_repo.get_all_accounts()
        heroes = self.hero_repo.get_all_heroes()
        players_items = self.player_items_repo.get_all_player_items()
        items = self.item_repo.get_all_items()

        for match in matches:
            st.subheader(f'ID матча: {match.id}')

            data = pd.DataFrame(
                [
                    {
                        'Время начала': match.start_time,
                        'Продолжительность': match.duration,
                        'Очки сил Света': match.radiant_kills,
                        'Очки сил Тьмы': match.dire_kills
                    }
                ]
            )
            st.dataframe(data, hide_index=True)

            match_players = [
                player
                for player in players
                if player.match_id == match.id
            ]

            if not match_players:
                continue

            st.write('**Участники матча**')

            players_side_by_side = []
            for player in match_players:
                print(player)
                side = 'силы Света' if player.is_radiant else 'силы Тьмы'

                nickname = next(
                    (
                        account.nickname
                        for account in accounts
                        if account.id == player.account_id
                    ),
                    'Никнейм отсутствует'
                )

                hero_name = next(
                    (
                        hero.name
                        for hero in heroes
                        if hero.id == player.hero_id
                    ),
                    'Имя героя отсутствует'
                )

                player_item_ids = [
                    player_item.item_id
                    for player_item in players_items
                    if player_item.player_id == player.id
                ]
                player_items = [
                    item.name
                    for item in items
                    if item.id in player_item_ids
                ]

                players_side_by_side.append(
                    {
                        'Никнейм': nickname,
                        'Герой': hero_name,
                        'Предметы':player_items,
                        'Количество убийств': player.kills,
                        'Количество смертей': player.deaths,
                        'Количество помощи': player.assistances,
                        'Выбор стороны': side
                    }
                )
            data = pd.DataFrame(players_side_by_side)
            st.dataframe(data, hide_index=True)

        if check_is_admin():
            self.create_match()

            match_ids = [match.id for match in matches]
            selected_id = st.selectbox(
                'Выберите ID матча для изменения', match_ids
            )
            selected_match = next(
                (match for match in matches if match.id == selected_id), None
            )

            if selected_match:
                st.write(f'**Выбран матч: {selected_match.id}**')
                self.update_match(selected_match)
                self.delete_match(selected_match)

    def create_match(self) -> None:
        st.write('**Добавление нового матча**')

        with st.form('create_match_form'):
            date_start = st.date_input('Дата начала матча')
            time_start = st.time_input('Время начала матча', value=time(0, 0))
            start_time = datetime.combine(date_start, time_start)

            duration_str = st.text_input(
                'Введите продолжительность матча (HH:mm:ss)', '00:00:00'
            )
            duration = convert_to_timedelta(duration_str)

            radiant_win = st.checkbox('В матче победили силы Света?')
            radiant_kills = st.number_input('Убийства сил Света', min_value=0)
            dire_kills = st.number_input('Убийства сил Тьмы', min_value=0)

            if st.form_submit_button('Создать матч'):
                new_match = Match(
                    start_time=start_time,
                    duration=duration,
                    radiant_win=radiant_win,
                    radiant_kills=radiant_kills,
                    dire_kills=dire_kills
                )
                try:
                    match_id = self.match_repo.add_match(new_match)
                    st.success(f'Матч успешно создан с ID: {match_id}')
                except Exception as e:
                    st.error(f'В ходе создания матча произошла ошибка: {e}')

    def update_match(self, selected_match) -> None:
        date_start = st.date_input('Новая дата начала матча')
        time_start = st.time_input('Новое время начала матча', value=time(0, 0))
        start_time = datetime.combine(date_start, time_start)

        duration_str = st.text_input(
            'Новая продолжительность матча (HH:mm:ss)', '00:00:00'
        )
        duration = convert_to_timedelta(duration_str)

        radiant_win = st.checkbox('В матче победили силы Света?')
        radiant_kills = st.number_input(
            'Новое количество убийства сил Света', min_value=0
        )
        dire_kills = st.number_input(
            'Новое количество убийства сил Тьмы', min_value=0
        )

        if st.button('Изменить матч'):
            try:
                updated_match = Match(
                    start_time=start_time,
                    duration=duration,
                    radiant_win=radiant_win,
                    radiant_kills=radiant_kills,
                    dire_kills=dire_kills
                )
                self.match_repo.update_match(selected_match.id, updated_match)
                st.success('Матч успешно обновлён!')
            except Exception as e:
                st.error(f'Произошла ошибка при обновлении матча: {e}')

    def delete_match(self, selected_match) -> None:
        if st.button('Удалить матч'):
            try:
                self.match_repo.delete_match(selected_match.id)
                st.success('Матч успешно удалён!')
            except Exception as e:
                st.error(f'Произошла ошибка при удалении предмета: {e}')
