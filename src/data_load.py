import pandas as pd
import os

def load_data(FILE_PATH):
    if not os.path.exists(FILE_PATH):
        print("Помилка: Файл не знайдено за шляхом {}".format(FILE_PATH))
        return None

    try:
        df = pd.read_excel(FILE_PATH, engine = "xlrd")
        print("Вивід інформації про датасет:")
        print("\nЗагальна інформація про датасет:")
        print(df.shape)
        print("\nІнформація про колонки:")
        print(df.info())
        print("\nПерші 5 рядків:")
        print(df.head())
        print("\nОстанні 5 рядків:")
        print(df.tail())

        return df

    except Exception as e:
        print("Помилка при зчитуванні файлу {}".format(e))
        return None

if __name__ == "__main__":
    FILE_PATH = "data/raw/dataset.xls"
    load_data(FILE_PATH)