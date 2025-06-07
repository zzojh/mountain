# traffic_predictor_app.py
import streamlit as st
import pandas as pd
import joblib  # 또는 pickle
from datetime import datetime

# 모델 불러오기
model = joblib.load('traffic_model.pkl')  # 미리 학습된 모델

st.title("📊 교통량 예측 앱")
st.markdown("날짜, 시간, 날씨 등의 정보를 입력하면 교통량을 예측해드립니다.")

# 입력 받기
date = st.date_input("날짜")
time = st.time_input("시간")
weather = st.selectbox("날씨", ["맑음", "흐림", "비", "눈"])

# 입력값 전처리
def preprocess_input(date, time, weather):
    dt = datetime.combine(date, time)
    features = {
        'hour': dt.hour,
        'weekday': dt.weekday(),
        'weather_code': {"맑음": 0, "흐림": 1, "비": 2, "눈": 3}[weather]
    }
    return pd.DataFrame([features])

# 예측 실행
if st.button("예측하기"):
    input_df = preprocess_input(date, time, weather)
    prediction = model.predict(input_df)
    st.success(f"예측된 교통량: **{int(prediction[0])} 대**")

