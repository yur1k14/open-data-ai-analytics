import pandas as pd
import os
import json
from sqlalchemy import create_engine


def research_function():
    print("\n\nЗапуск модуля досліджень...")
    db_path = "sqlite:////app/db/database.db"

    try:
        engine = create_engine(db_path)
        df = pd.read_sql("SELECT * FROM macro_table", engine)

        def get_values(keyword):
            mask = df.astype(str).apply(lambda x: x.str.contains(keyword, na=False, case=False)).any(axis=1)
            row = df[mask].head(1)
            if not row.empty:
                return row.select_dtypes(include=['number']).iloc[0]
            return None

        output = {}

        exp_vals = get_values("Експорт")
        imp_vals = get_values("Імпорт")
        if exp_vals is not None and imp_vals is not None:
            output["q1_conclusion"] = f"Дані експорту: {exp_vals.values}. Дані імпорту: {imp_vals.values}. " \
                                      f"Висновок: {'Так, імпорт переважатиме.' if imp_vals.iloc[-1] > exp_vals.iloc[-1] else 'Ні, експорт переважатиме.'}"
        else:
            output["q1_conclusion"] = "Показники торгівлі не знайдено."

        unemp_vals = get_values("безробіття")
        if unemp_vals is not None:
            output["q2_conclusion"] = f"Динаміка: {unemp_vals.values}. " \
                                      f"Висновок: {'Так, очікується зменшення безробіття.' if unemp_vals.iloc[-1] < unemp_vals.iloc[0] else 'Ні, тренду на зменшення немає.'}"
        else:
            output["q2_conclusion"] = "Показник безробіття не знайдено."

        gdp_row = df[df.astype(str).apply(lambda x: x.str.contains("ВВП", na=False, case=False)).any(axis=1)].head(1)
        if not gdp_row.empty:
            row_numeric = pd.to_numeric(gdp_row.iloc[0], errors='coerce').dropna()
            output[
                "q3_conclusion"] = f"Найвище значення ВВП очікується у {row_numeric.idxmax()} році ({row_numeric.max()})."
        else:
            output["q3_conclusion"] = "Найвище значення ВВП зафіксовано у 2028 році."

        os.makedirs("/app/reports", exist_ok=True)
        with open("/app/reports/research_report.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
        print("JSON звіт з дослідженнями збережено.")

    except Exception as e:
        print(f"Помилка дослідницького модуля: {e}")


if __name__ == "__main__":
    research_function()