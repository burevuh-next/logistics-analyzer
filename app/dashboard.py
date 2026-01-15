import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('📊 Logistics Analyzer Dashboard')
st.write("Анализ логистических данных в реальном времени")

# Загрузка файла
uploaded_file = st.file_uploader("Загрузите CSV файл", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(f"Загружено {len(df)} записей")
    
    # Показ данных
    if st.checkbox("Показать данные"):
        st.dataframe(df)
    
    # Графики
    st.subheader("📈 Визуализация")
    fig, ax = plt.subplots()
    df.groupby('carrier')['cost_rub'].sum().plot(kind='bar', ax=ax)
    st.pyplot(fig)
