import streamlit as st
import toml
import bcrypt


def authenticate():
    """
    Ручная аутентификация пользователя: форма ввода логина и пароля.
    Проверка bcrypt-хеша из secrets.toml. После успешного входа ставит st.session_state['authenticated']=True.
    """
    # Инициализация статуса аутентификации
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # Если пользователь не аутентифицирован, показываем форму
    if not st.session_state['authenticated']:
        # Загружаем учетные данные
        try:
            config = toml.load('secrets.toml')
            credentials = config.get('credentials', {})
        except Exception:
            st.error('Не удалось загрузить файл с учетными данными.')
            st.stop()

        st.title('Вход')
        username = st.text_input('Логин')
        password = st.text_input('Пароль', type='password')

        if st.button('Login'):
            if username in credentials:
                hashed = credentials[username]['password']
                if bcrypt.checkpw(password.encode(), hashed.encode()):
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.experimental_rerun()
                else:
                    st.error('Неверное имя пользователя или пароль')
            else:
                st.error('Неверное имя пользователя или пароль')

        # Останавливаем дальнейшее выполнение
        st.stop()
