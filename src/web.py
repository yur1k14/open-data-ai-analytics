import streamlit as st
import os
import json

st.set_page_config(page_title="AI Analytics Dashboard", layout="wide")
st.title("📊 Панель аналітики відкритих даних України (2026-2028)")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.header("📋 Звіти аналітичних модулів")

    st.subheader("Перевірка якості даних")
    if os.path.exists("/app/reports/quality_report.txt"):
        with open("/app/reports/quality_report.txt", "r", encoding="utf-8") as f:
            st.text(f.read())
    else:
        st.info("Очікування генерації звіту якості...")

    st.subheader("Економічне дослідження")
    if os.path.exists("/app/reports/research_report.json"):
        with open("/app/reports/research_report.json", "r", encoding="utf-8") as f:
            res = json.load(f)
            st.info(f"**Теза 1 (Торгівля):** {res.get('q1_conclusion', 'Немає даних')}")
            st.info(f"**Теза 2 (Безробіття):** {res.get('q2_conclusion', 'Немає даних')}")
            st.info(f"**Теза 3 (Пік ВВП):** {res.get('q3_conclusion', 'Немає даних')}")
    else:
        st.info("Очікування результатів дослідження...")

with col2:
    st.header("📉 Візуалізація прогнозів")
    img_path = "/app/reports/figures/economic_analysis.png"
    if os.path.exists(img_path):
        st.image(img_path, caption="Порівняння експорту/імпорту та тренд безробіття")
    else:
        st.info("Графіки ще генеруються...")