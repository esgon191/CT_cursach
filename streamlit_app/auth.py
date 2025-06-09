import streamlit as st
import streamlit_authenticator as stauth
import toml


def authenticate():
    """
    Проводит аутентификацию пользователя через streamlit-authenticator.
    После успешного логина устанавливает st.session_state['authenticated'] = True.
    Использует простую проверку переменной session_state['username'].
    """
    if "authenticated" not in st.session_state:
        # Загружаем учетные данные из secrets.toml
        try:
            config = toml.load("secrets.toml")
            credentials = config.get("credentials", {})
        except Exception:
            st.error("Не удалось загрузить файл с учетными данными.")
            st.stop()

        # Формируем словарь для аутентификатора
        usernames = list(credentials.keys())
        user_info = {user: {"name": credentials[user].get("name", user),
                            "password": credentials[user]["password"]}
                     for user in usernames}

        # Инициализация аутентификатора
        authenticator = stauth.Authenticate(
            {"usernames": user_info},
            cookie_name="streamlit_auth",
            key="some_random_key",
            cookie_expiry_days=1
        )

        # Отображаем форму логина. Возвращаемые значения игнорируем, смотрим в st.session_state
        authenticator.login("Login")

        # Проверяем статус из session_state, установленные самим аутентификатором
        auth_status = st.session_state.get("authentication_status")
        username = st.session_state.get("username")

        if auth_status:
            # Успешный логин
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
        elif auth_status is False:
            # Неверные учётные данные
            st.error("Неверное имя пользователя или пароль")
            st.session_state['authenticated'] = False
            st.stop()
        else:
            # auth_status is None — пользователь ещё не залогинен
            st.session_state['authenticated'] = False
            st.stop()
