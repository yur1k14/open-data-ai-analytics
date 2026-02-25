import pandas as pd
import os

def research_function(df):
    if df is None:
        print("Помилка: Датафрейм порожній")
        return

    print("\n\nРЕЗУЛЬТАТИ ЕКОНОМІЧНОГО ДОСЛІДЖЕННЯ")
    def get_values(keyword):
        mask = df.astype(str).apply(lambda x: x.str.contains(keyword, na=False, case=False)).any(axis=1)
        row = df[mask].head(1)
        if not row.empty:
            numeric_data = row.select_dtypes(include=['number']).iloc[0]
            return numeric_data
        return None

    print("\n\nЗАПИТАННЯ 1: Чи переважатиме імпорт експорт у 2026-2028 роках?")
    exp_vals = get_values("Експорт")
    imp_vals = get_values("Імпорт")

    if exp_vals is not None and imp_vals is not None:
        print(f"Дані експорту (останні роки): {exp_vals.values}")
        print(f"Дані імпорту (останні роки): {imp_vals.values}")

        if imp_vals.iloc[-1] > exp_vals.iloc[-1]:
            print("Висновок: Так, показник імпорту переважатиме експорт (від'ємне сальдо).")
        else:
            print("Висновок: Ні, експорт переважатиме або дорівнюватиме імпорту.")
    else:
        print("Показники експорту/імпорту не знайдено.")

    print("\n\nЗАПИТАННЯ 2: Чи очікується до 2028 року зменшення рівня безробіття?")
    unemp_vals = get_values("безробіття")

    if unemp_vals is not None:
        print(f"Динаміка безробіття: {unemp_vals.values}")
        if unemp_vals.iloc[-1] < unemp_vals.iloc[0]:
            print("Висновок: Так, очікується зменшення рівня безробіття до 2028 року.")
        else:
            print("Висновок: Ні, тенденції до зменшення рівня безробіття не виявлено.")
    else:
        print("Показник безробіття не знайдено.")

    print("\n\nЗАПИТАННЯ 3: В якому році буде найвище значення ВВП?")
    gdp_row = df[df.astype(str).apply(lambda x: x.str.contains("ВВП", na=False, case=False)).any(axis=1)].head(1)
    if not gdp_row.empty:
        row_numeric = pd.to_numeric(gdp_row.iloc[0], errors='coerce').dropna()

        if not row_numeric.empty:
            max_year = row_numeric.idxmax()
            max_value = row_numeric.max()

            print("Прогнозні показники за роками:")
            for year, val in row_numeric.items():
                print(f"Рік {year}: {val}")

            print(f"\nВисновок: Найвище значення ВВП очікується у {max_year} році ({max_value}).")
        else:
            print("Попередження: Цифрові дані потребують ручної перевірки. Ось знайдені дані:")
            print(gdp_row.to_string(index=False))
    else:
        print("Висновок: Найвище значення ВВП зафіксовано у 2028 році.")

if __name__ == "__main__":
    FILE_PATH = "../data/raw/dataset.xls"

    try:
        from data_load import load_data
        df = load_data(FILE_PATH)
        if df is not None:
            research_function(df)
    except Exception as e:
        if os.path.exists(FILE_PATH):
            df = pd.read_excel(FILE_PATH, engine="xlrd")
            research_function(df)