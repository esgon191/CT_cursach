import pandas as pd
import numpy as np

def validate_csv(df: pd.DataFrame) -> bool:
    """
    Проверяет DataFrame на соответствие требуемому формату.
    Здесь можно добавить проверку колонок, типов и т.д.
    Возвращает True, если формат корректен, иначе False.
    """
    # TODO: реализовать проверку формата CSV.
    # Пример: убедиться, что есть нужные колонки
    required_columns = []  # Список названий обязательных колонок
    if len(df) == 500 and len(df.columns) == 10:
        return True
    # Другие проверки можно добавить здесь
    return False

def df_to_json(df: pd.DataFrame) -> dict:
    inputs = {}
    for i in range(10):
        # Формируем имя ключа (args_0, args_0_1, ..., args_0_9)
        key = f"args_0_{i}" if i > 0 else "args_0"
        
        # Берём i-ю колонку, преобразуем в массив [1, 500, 1]
        column_data = df.iloc[:, i].values.astype(np.float32)
        reshaped_data = column_data.reshape(1, 500, 1)  # Форма [1, 500, 1]
        
        inputs[key] = reshaped_data.tolist()  # Для REST-запроса

    return inputs