import pandas as pd

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
    FILE_PATH = "../data/raw/dataset.xls"

    try:
        from data_load import load_data
        df = load_data(FILE_PATH)
        check_data_quality(df)

    except ImportError as e:
        df = pd.read_excel(FILE_PATH, engine = "xlrd")
        check_data_quality(df)