import streamlit as st
import pandas as pd

from repositories.item import ItemRepository
from services.utils import check_is_admin


class ItemView:
    def __init__(self) -> None:
        self.repo = ItemRepository()

    def show_items(self) -> None:
        st.header('Список всех предметов')

        items = self.repo.get_all_items()

        if not items:
            st.info('В базе данных нет предметов')
            return

        data = pd.DataFrame(
            [
                {'ID': item.id, 'Название': item.name}
                for item in items
            ]
        )
        st.dataframe(data, hide_index=True)

        if check_is_admin():
            self.create_item()

            item_ids = [hero.id for hero in items]
            selected_id = st.selectbox(
                'Выберите ID предмета для изменения', item_ids
            )
            selected_item = next(
                (item for item in items if item.id == selected_id), None
            )

            if selected_item:
                st.write(f'Выбран предмет: {selected_item.name}')
                self.update_item(selected_item)
                self.delete_item(selected_item)

    def create_item(self) -> None:
        st.write('Добавление нового предмета')

        items = self.repo.get_all_items()

        with st.form('create_item_form'):
            name = st.text_input('Название предмета', '')

            if st.form_submit_button('Добавить предмет'):
                if name.strip():
                    try:
                        hero_id = self.repo.add_item(name.strip())
                        st.success(f'Предмет успешно создан! ID: {hero_id}')
                    except Exception as e:
                        st.error(
                            f'Произошла ошибка при добавлении предмета: {e}'
                        )
                else:
                    st.warning('Название предмета не может быть пустым!')

    def update_item(self, selected_item) -> None:
        items = self.repo.get_all_items()

        new_name = st.text_input('Новое название предмета', selected_item.name)

        if st.button('Изменить предмет'):
            if new_name.strip():
                try:
                    self.repo.update_item(selected_item.id, new_name.strip())
                    st.success('Предмет успешно обновлён!')
                except Exception as e:
                    st.error(f'Произошла ошибка при обновлении предмета: {e}')
            else:
                st.warning('Название предмета не может быть пустым!')

    def delete_item(self, selected_item) -> None:
        if st.button('Удалить предмет'):
            try:
                self.repo.delete_item(selected_item.id)
                st.success('Предмет успешно удалён!')
            except Exception as e:
                st.error(f'Произошла ошибка при удалении предмета: {e}')
