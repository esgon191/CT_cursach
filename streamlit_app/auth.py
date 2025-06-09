import streamlit as st
import streamlit_authenticator as stauth
import toml


def authenticate():
    """
    Проводит аутентификацию пользователя через streamlit-authenticator.
    После успешного логина устанавливает st.session_state['authenticated'] = True.
    """
    if "authenticated" not in st.session_state:
        # Загружаем учетные данные из secrets.toml
        try:
            config = toml.load("secrets.toml")
            credentials = config["credentials"]
        except Exception as e:
            st.error("Не удалось загрузить файл с учетными данными.")
            st.stop()

        # Подготавливаем данные для аутентификации
        usernames = list(credentials.keys())
        user_info = {}
        for user in usernames:
            user_info[user] = {
                "name": credentials[user].get("name", user),
                "password": credentials[user]["password"]
            }

        # Инициализация аутентификатора
        authenticator = stauth.Authenticate(
            {"usernames": user_info},
            cookie_name="streamlit_auth",  # имя куки
            key="some_random_key",        # секретный ключ
            cookie_expiry_days=1
        )

        # Отображаем форму логина
        name, auth_status, username = authenticator.login("Login", "main")
        
        if auth_status:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
        elif auth_status is False:
            st.error("Неверное имя пользователя или пароль")
            st.session_state["authenticated"] = False
        else:
            # auth_status is None (пользователь еще не залогинен)
            st.session_state["authenticated"] = False
            st.stop()
