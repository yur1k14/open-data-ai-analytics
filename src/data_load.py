import pandas as pd
import os
from sqlalchemy import create_engine


def load_data(FILE_PATH):
    if not os.path.exists(FILE_PATH):
        print(f"Помилка: Файл не знайдено за шляхом {FILE_PATH}")
        return None

    try:
        df = pd.read_excel(FILE_PATH, engine="xlrd")
        print("Вивід інформації про датасет:")
        print(f"Розмір: {df.shape}")

        db_path = "sqlite:////app/db/database.db"
        os.makedirs("/app/db", exist_ok=True)

        engine = create_engine(db_path)
        df.to_sql('macro_table', engine, if_exists='replace', index=False)
        print("Дані успішно збережено у спільну БД SQLite!")
        return df

    except Exception as e:
        print(f"Помилка при зчитуванні/записі файлу: {e}")
        return None


if __name__ == "__main__":
    FILE_PATH = "data/raw/dataset.xls"
    load_data(FILE_PATH)