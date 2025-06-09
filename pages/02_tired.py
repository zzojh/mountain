import streamlit as st
import pandas as pd

# 🖥️ Streamlit 앱
st.title("🚗 교통량 예측기")

hour = st.slider("시간대 (0~23)", 0, 23, 8)
temp = st.number_input("기온 (°C)", value=20.0)

if st.button("예측하기"):
    pred = model.predict([[hour, temp]])
    st.success(f"예상 교통량: {int(pred[0]):,} 대")

