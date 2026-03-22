import pandas as pd
import matplotlib.pyplot as plt
import os

def create_visualizations(df):
    if df is None:
        print("Помилка: Дані для візуалізації відсутні.")
        return

    plt.style.use('fast')

    def get_data(keyword):
        # Перетворюємо дані на текст для пошуку, щоб уникнути помилок з типами даних
        mask = df.astype(str).apply(lambda x: x.str.contains(keyword, na=False, case=False)).any(axis=1)
        row = df[mask].head(1)
        if not row.empty:
            return pd.to_numeric(row.select_dtypes(include=['number']).iloc[0], errors='coerce').dropna()
        return None

    # Отримання даних для решти показників
    export = get_data("Експорт")
    import_data = get_data("Імпорт")
    unemployment = get_data("безробіття")

    # Змінюємо кількість підграфіків з 3 на 2
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 1. Графік: Торговельний баланс (Експорт vs Імпорт)
    if export is not None and import_data is not None:
        trade_df = pd.DataFrame({'Експорт': export, 'Імпорт': import_data})
        trade_df.plot(kind='bar', ax=ax1, color=['#3498db', '#95a5a6'])
        ax1.set_title('Експорт та Імпорт (2026-2028)')
        ax1.set_ylabel('Значення')
        ax1.legend()
    else:
        ax1.set_title('Дані для торгівлі не знайдено')

    # 2. Графік: Рівень безробіття
    if unemployment is not None:
        unemployment.plot(kind='line', marker='s', color='#e74c3c', linewidth=2, ax=ax2)
        ax2.set_title('Динаміка безробіття (%)')
        ax2.grid(True, linestyle='--', alpha=0.6)
    else:
        ax2.set_title('Дані безробіття не знайдено')

    plt.tight_layout()

    # Збереження результату у папку звітів
    os.makedirs('reports/figures', exist_ok=True)
    report_path = 'reports/figures/economic_analysis_no_gdp.png'
    plt.savefig(report_path)

    print("-" * 40)
    print(f"Візуальний звіт (без ВВП) збережено: {report_path}")
    print("-" * 40)
    plt.show()

if __name__ == "__main__":
    from data_load import load_data
    FILE_PATH = "data/raw/dataset.xls"

    try:
        # Спроба завантаження через створений раніше модуль
        df = load_data(FILE_PATH)
        create_visualizations(df)
    except Exception as e:
        # Резервний метод завантаження безпосередньо через pandas
        if os.path.exists(FILE_PATH):
            df = pd.read_excel(FILE_PATH, engine="xlrd")
            create_visualizations(df)
        else:
            print(f"Файл не знайдено за шляхом: {FILE_PATH}")