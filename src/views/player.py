import streamlit as st

import pandas as pd

from repositories.account import AccountRepository
from repositories.match import MatchRepository
from repositories.player import PlayerRepository
from repositories.user import UserRepository

from models.player import Player
from services.utils import check_is_admin


class PlayerView:
    def __init__(self) -> None:
        self.match_repo = MatchRepository()
        self.user_repo = UserRepository()
        self.player_repo = PlayerRepository()
        self.account_repo = AccountRepository()

    def show_player_list(self):
        st.header('Список участников матчей')

        if not check_is_admin():
            return

        self.create_player()

        players = self.player_repo.get_all_players()
        print(players)

        if not players:
            st.info('Участники матчей не найдены')

        data = pd.DataFrame(players)
        st.dataframe(data, hide_index=True)

        player_ids = [player.id for player in players]
        selected_id = st.selectbox(
            'Выберите ID участника матча для удаления', player_ids
        )
        selected_player = next(
            (player for player in players if player.id == selected_id), None
        )

        if selected_player:
            st.write(f'**Выбран участник матча: {selected_player.id}**')
            self.delete_player(selected_player)

    def create_player(self):
        st.write('**Создание участника матча**')

        matches = self.match_repo.get_all_matches()
        match_options = {f"Матч ID {match.id}": match.id for match in matches}

        nickname = st.text_input("Никнейм")
        match_id = st.selectbox("ID матча", options=match_options.keys())
        hero_id = st.number_input("ID героя", min_value=1)
        is_radiant = st.checkbox("Является игроком сил Света?")

        kills = st.number_input("Количество убийств", min_value=0)
        deaths = st.number_input("Количество смертей", min_value=0)
        assistances = st.number_input("Количество ассистов", min_value=0)
        rating_change = st.number_input(
            "Изменение рейтинга", min_value=0, max_value=100
        )

        if st.button("Создать игрока"):
            accounts = self.account_repo.get_all_accounts()

            account_id = next(
                (
                    account.id
                    for account in accounts
                    if account.nickname == nickname
                ),
                None
            )

            if not account_id:
                st.error('Аккаунта с таким никнеймом не найден')

            new_player = Player(
                account_id=account_id,
                match_id=match_options[match_id],
                hero_id=int(hero_id),
                kills=int(kills),
                deaths=int(deaths),
                assistances=int(assistances),
                is_radiant=is_radiant,
                rating_change=int(rating_change)
            )
            player_id = self.player_repo.add_player(new_player)
            st.success(f"Игрок успешно создан с ID: {player_id}")

    def delete_player(self, selected_player) -> None:
        if st.button('Удалить участника матча'):
            try:
                self.player_repo.delete_player(selected_player.id)
                st.success('Игрок успешно удалён!')
            except Exception as e:
                st.error(f'Произошла ошибка при удалении игрока: {e}')
