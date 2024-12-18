import streamlit as st
import pandas as pd

from repositories.hero import HeroRepository
from services.utils import check_is_admin


class HeroView:
    def __init__(self):
        self.repo = HeroRepository()

    def show_heroes(self) -> None:
        st.header('Список всех героев')

        heroes = self.repo.get_all_heroes()

        if not heroes:
            st.info('В базе данных нет героев')
            return

        data = pd.DataFrame(
            [
                {'ID': hero.id, 'Имя': hero.name}
                for hero in heroes
            ]
        )
        st.dataframe(data, hide_index=True)

        if check_is_admin():
            self.create_hero()

            hero_ids = [hero.id for hero in heroes]
            selected_id = st.selectbox(
                'Выберите ID героя для изменения', hero_ids
            )
            selected_hero = next(
                (hero for hero in heroes if hero.id == selected_id), None
            )

            if selected_hero:
                st.write(f'Выбран герой: {selected_hero.name}')
                self.update_hero(selected_hero)
                self.delete_hero(selected_hero)

    def create_hero(self) -> None:
        st.write('Добавление нового героя')

        with st.form('create_hero_form'):
            name = st.text_input('Имя героя', '')

            if st.form_submit_button('Добавить героя'):
                if name.strip():
                    try:
                        hero_id = self.repo.add_hero(name.strip())
                        st.success(f'Герой успешно создан! ID: {hero_id}')
                    except Exception as e:
                        st.error(f'Произошла ошибка при добавлении героя: {e}')
                else:
                    st.warning('Имя героя не может быть пустым!')

    def update_hero(self, selected_hero) -> None:
        new_name = st.text_input('Новое имя героя', selected_hero.name)

        if st.button('Изменить героя'):
            if new_name.strip():
                try:
                    self.repo.update_hero(selected_hero.id, new_name.strip())
                    st.success('Герой успешно обновлён!')
                except Exception as e:
                    st.error(f'Произошла ошибка при обновлении героя: {e}')
            else:
                st.warning('Имя героя не может быть пустым!')

    def delete_hero(self, selected_hero) -> None:
        if st.button('Удалить героя'):
            try:
                self.repo.delete_hero(selected_hero.id)
                st.success('Герой успешно удалён!')
            except Exception as e:
                st.error(f'Произошла ошибка при удалении героя: {e}')
