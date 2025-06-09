import streamlit as st
import pandas as pd
from utils import validate_csv


def render_ui():
    """
    Рендерит UI для загрузки CSV и кнопки submit.
    Возвращает pandas.DataFrame при успешной загрузке и валидации, иначе None.
    """
    st.header("Шаг 1: Загрузка CSV")
    uploaded_file = st.file_uploader("Выберите CSV файл", type="csv")
    if not uploaded_file:
        return None

    # Пытаемся прочитать CSV
    try:
        df = pd.read_csv(uploaded_file)
    except Exception:
        st.error("Не удалось прочитать CSV файл. Убедитесь, что это корректный CSV.")
        return None

    # Кнопка отправки
    if st.button("Submit"):
        # Валидация формата файла
        if not validate_csv(df):
            st.error("Формат файла не соответствует требуемому.")
            return None
        # Если всё ок, возвращаем DataFrame
        return df

    return None
