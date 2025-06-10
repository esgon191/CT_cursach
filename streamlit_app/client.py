import os
import requests
import streamlit as st
import pandas as pd

from utils import df_to_json

def predict(df: pd.DataFrame):
    """
    Отправляет DataFrame на TensorFlow-Serving и возвращает предсказание (одно число) или None при ошибке.
    """
    # URL сервиса TF-Serving: можно задать через переменную окружения
    tf_server_url = os.getenv(
        "TF_SERVER_URL",
        "http://tfserving:8501/v1/models/saved_model:predict"
    )

    # Формируем полезную нагрузку для REST API
    payload = {"inputs": df_to_json(df)}

    try:
        response = requests.post(tf_server_url, json=payload)
        response.raise_for_status()
    except Exception as e:
        st.error(f"Ошибка при запросе к модели: {e}")
        return None

    # Разбираем ответ
    data = response.json()
    predictions = data.get("predictions")
    if predictions is None or len(predictions) == 0:
        st.error("Некорректный ответ от сервера модели.")
        return None

    # Предполагаем, что модель возвращает список списков или список чисел
    pred = predictions[0]
    # Если предсказание — список, берем первый элемент
    if isinstance(pred, (list, tuple)):
        return pred[0]
    return pred
