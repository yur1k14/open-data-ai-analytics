import pandas as pd
import os
from sqlalchemy import create_engine


def check_data_quality():
    print("\n\nЗапуск модуля перевірки якості даних...")
    db_path = "sqlite:////app/db/database.db"

    try:
        engine = create_engine(db_path)
        df = pd.read_sql("SELECT * FROM macro_table", engine)

        miss = df.isnull().sum()
        duplicate = df.duplicated()

        report = "=== АНАЛІЗ ЯКОСТІ ДАНИХ (DOCKER) ===\n\n"
        if miss.sum() > 0:
            report += f"Кількість пропущених значень: {miss.sum()}\n"
        else:
            report += "Пропущені дані відсутні\n"

        if duplicate.sum() > 0:
            report += f"Кількість дублікатів: {duplicate.sum()}\n"
        else:
            report += "Дублікати відсутні\n"

        report += f"\nТипи даних колонок:\n{df.dtypes.to_string()}\n"

        os.makedirs("/app/reports", exist_ok=True)
        with open("/app/reports/quality_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print("Звіт з якості збережено в текстовий файл.")

    except Exception as e:
        print(f"Критична помилка аналізу якості: {e}")


if __name__ == "__main__":
    check_data_quality()