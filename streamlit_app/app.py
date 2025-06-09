import streamlit as st
from auth import authenticate
from ui import render_ui
from client import predict


def main():
    # Модуль аутентификации: отображение формы и проверка
    authenticate()
    if not st.session_state.get("authenticated"):
        return

    # Основной интерфейс: загрузка CSV и инференс
    df = render_ui()
    if df is not None:
        # Отправляем данные в модель и отображаем результат
        result = predict(df)
        st.write("## Результат инференса:")
        st.write(result)


if __name__ == "__main__":
    main()
