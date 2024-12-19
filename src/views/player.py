import streamlit as st

import pandas as pd

from repositories.account import AccountRepository
from repositories.hero import HeroRepository
from repositories.item import ItemRepository
from repositories.match import MatchRepository
from repositories.player import PlayerRepository
from repositories.player_items import PlayerItemsRepository
from repositories.user import UserRepository

from models.player import Player
from services.utils import check_is_admin


class PlayerView:
    def __init__(self) -> None:
        self.match_repo = MatchRepository()
        self.user_repo = UserRepository()
        self.player_repo = PlayerRepository()
        self.account_repo = AccountRepository()
        self.hero_repo = HeroRepository()
        self.item_repo = ItemRepository()
        self.player_item_repo = PlayerItemsRepository()

    def show_player_list(self):
        st.header('Список участников матчей')

        if not check_is_admin():
            return

        self.create_player()

        players = self.player_repo.get_all_players()

        if not players:
            st.info('Участники матчей не найдены')

        data = []

        for player in players:
            nickname = (
                self.account_repo.get_account_by_id(player.account_id).nickname
            )
            hero_name = self.hero_repo.get_hero_by_id(player.hero_id).name
            player_item_ids = [
                player_item.id
                for player_item in self.player_item_repo.get_items_by_player(player.id)
            ]
            item_names = [
                item.name
                for item in self.item_repo.get_all_items()
                if item.id in player_item_ids
            ]
            player_side = 'силы Света' if player.is_radiant else 'силы Тьмы'

            data.append(
                {
                    'ID участника матча': player.id,
                    'Никнейм': nickname,
                    'ID матча': player.match_id,
                    'Герой': hero_name,
                    'Предметы': item_names,
                    'Убийства': player.kills,
                    'Смерти': player.deaths,
                    'Помощи': player.assistances,
                    'Сторона': player_side,
                    'Изменение рейтинга': player.rating_change
                }
            )

        st.dataframe(pd.DataFrame(data), hide_index=True)

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
        match_options = {f'Матч ID {match.id}': match.id for match in matches}

        accounts = self.account_repo.get_all_accounts()
        nickname = st.selectbox(
            'Никнейм', options=[account.nickname for account in accounts]
        )
        account_id = next(
            (
                account.id
                for account in accounts
                if account.nickname == nickname
            ),
            None
        )

        match_id = st.selectbox('ID матча', options=match_options.keys())

        heroes = self.hero_repo.get_all_heroes()
        hero_name = st.selectbox('Герой', options=[hero.name for hero in heroes])
        hero_id = next(
            (hero.id for hero in heroes if hero.name == hero_name), None
        )

        items = self.item_repo.get_all_items()
        item_names = st.multiselect(
            'Предметы', options=[item.name for item in items]
        )
        item_ids = [item.id for item in items if item.name in item_names]

        is_radiant = st.checkbox('Является игроком сил Света?')

        kills = st.number_input('Количество убийств', min_value=0)
        deaths = st.number_input('Количество смертей', min_value=0)
        assistances = st.number_input('Количество помощи', min_value=0)
        rating_change = st.number_input(
            'Изменение рейтинга', min_value=-100, max_value=100
        )

        if st.button('Создать игрока'):
            players = self.player_repo.get_all_players()
            this_match_players = [
                player
                for player in players
                if player.match_id == match_options[match_id]
            ]

            if account_id in [player.account_id for player in this_match_players]:
                st.error('Игрок уже является участником данного матча')
                return

            if hero_id in [player.hero_id for player in this_match_players]:
                st.error('Герой уже выбран другим игроком')
                return

            this_match = self.match_repo.get_match_by_id(
                match_options[match_id]
            )
            if this_match.radiant_win:
                if is_radiant and rating_change <= 0:
                    st.error(
                        'Изменение рейтинга победившего игрока '
                        'должно быть положительным'
                    )
                    return
                if not is_radiant and rating_change >= 0:
                    st.error(
                        'Изменение рейтинга проигравшего игрока '
                        'должно быть отрицательным'
                    )
                    return
            else:
                if is_radiant and rating_change >= 0:
                    st.error(
                        'Изменение рейтинга проигравшего игрока '
                        'должно быть отрицательным'
                    )
                    return
                if not is_radiant and rating_change <= 0:
                    st.error(
                        'Изменение рейтинга победившего игрока '
                        'должно быть положительным'
                    )
                    return

            this_match_radiant_players = []
            this_match_dire_players = []
            for player in this_match_players:
                if player.is_radiant:
                    this_match_radiant_players.append(player)
                else:
                    this_match_dire_players.append(player)

            if is_radiant:
                if len(this_match_radiant_players) + 1 > 5:
                    st.error(
                        'В матче присутствует максимальное количество '
                        'игроков сил Света'
                    )
                    return
            else:
                if len(this_match_dire_players) + 1 > 5:
                    st.error(
                        'В матче присутствует максимальное количество '
                        'игроков сил Тьмы'
                    )
                    return

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

            for item_id in item_ids:
                self.player_item_repo.add_item_to_player(player_id, item_id)

            st.success(f'Игрок успешно создан с ID: {player_id}')

    def delete_player(self, selected_player) -> None:
        if st.button('Удалить участника матча'):
            try:
                self.player_repo.delete_player(selected_player.id)
                st.success('Игрок успешно удалён!')
            except Exception as e:
                st.error(f'Произошла ошибка при удалении игрока: {e}')
