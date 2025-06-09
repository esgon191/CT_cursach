# streamlit_app/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Скопировать зависимости и установить их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать весь код приложения
COPY . .

# Открываем порт Streamlit
EXPOSE 8501

# Запуск Streamlit при старте контейнера
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.enableXsrfProtection=true"]
