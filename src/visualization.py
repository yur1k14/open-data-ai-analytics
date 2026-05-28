import pandas as pd
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine


def create_visualizations():
    print("\n\nЗапуск модуля візуалізації...")
    db_path = "sqlite:////app/db/database.db"

    try:
        engine = create_engine(db_path)
        df = pd.read_sql("SELECT * FROM macro_table", engine)
        plt.style.use('fast')

        def get_data(keyword):
            mask = df.astype(str).apply(lambda x: x.str.contains(keyword, na=False, case=False)).any(axis=1)
            row = df[mask].head(1)
            if not row.empty:
                return pd.to_numeric(row.select_dtypes(include=['number']).iloc[0], errors='coerce').dropna()
            return None

        export = get_data("Експорт")
        import_data = get_data("Імпорт")
        unemployment = get_data("безробіття")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        if export is not None and import_data is not None:
            trade_df = pd.DataFrame({'Експорт': export, 'Імпорт': import_data})
            trade_df.plot(kind='bar', ax=ax1, color=['#3498db', '#95a5a6'])
            ax1.set_title('Експорт та Імпорт (2026-2028)')
            ax1.set_ylabel('Значення')
            ax1.legend()

        if unemployment is not None:
            unemployment.plot(kind='line', marker='s', color='#e74c3c', linewidth=2, ax=ax2)
            ax2.set_title('Динаміка безробіття (%)')
            ax2.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout()

        os.makedirs('/app/reports/figures', exist_ok=True)
        plt.savefig('/app/reports/figures/economic_analysis.png')
        plt.close()
        print("Графічний звіт збережено.")

    except Exception as e:
        print(f"Помилка візуалізації: {e}")


if __name__ == "__main__":
    create_visualizations()