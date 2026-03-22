import pandas as pd
import os

def check_data_quality(df):
    miss = df.isnull().sum()
    duplicate = df.duplicated()

    print("\n\nАналіз датасету")
    if miss.sum() > 0:
        print("\nКількість пропущених значень: ", miss.sum())
    else:
        print("\nПропущені дані відсутні")

    if duplicate.sum() > 0:
        print("\nКількість дублікатів: ", duplicate.sum())
    else:
        print("\nДублікати відсутні")

    print("\nТипи даних")
    print(df.dtypes)


if __name__ == "__main__":
    FILE_PATH = "data/raw/dataset.xls"

    try:
        from data_load import load_data
        df = load_data(FILE_PATH)
        if df is not None:
            check_data_quality(df)
        else:
            print(f"Помилка: load_data повернула None для {FILE_PATH}")

    except Exception as e:
        print(f"Спроба прямого зчитування через pandas через помилку: {e}")
        if os.path.exists(FILE_PATH):
            df = pd.read_excel(FILE_PATH, engine="xlrd")
            check_data_quality(df)
        else:
            print(f"Критична помилка: Файл {FILE_PATH} взагалі відсутній на диску.")