import streamlit as st
import pickle
import numpy as np

# 모델 불러오기
with open('traffic_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("🚗 교통량 예측 앱")

# 사용자 입력
hour = st.slider("시간 (0~23)", 0, 23, 8)
day_of_week = st.selectbox("요일", [0, 1, 2, 3, 4, 5, 6], format_func=lambda x: ["월", "화", "수", "목", "금", "토", "일"][x])
temperature = st.number_input("기온 (°C)", min_value=-30.0, max_value=50.0, value=20.0)
weather = st.selectbox("날씨", [1, 2, 3, 4], format_func=lambda x: {1: "맑음", 2: "흐림", 3: "비", 4: "눈"}[x])

# 예측
input_data = np.array([[hour, day_of_week, temperature, weather]])
prediction = model.predict(input_data)

st.subheader("📈 예측된 교통량:")
st.success(f"{int(prediction[0])} 대")
