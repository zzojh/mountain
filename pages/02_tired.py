import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# 📌 간단한 학습용 데이터
data = {
    "hour": [8, 9, 10, 11, 12, 13, 14],
    "temperature": [15.0, 17.0, 20.0, 22.0, 24.0, 25.0, 26.0],
    "traffic_volume": [320, 450, 600, 700, 750, 720, 690]
}
df = pd.DataFrame(data)

# 🎯 모델 학습
model = LinearRegression()
model.fit(df[["hour", "temperature"]], df["traffic_volume"])

# 🖥️ Streamlit 앱
st.title("🚗 교통량 예측기")

hour = st.slider("시간대 (0~23)", 0, 23, 8)
temp = st.number_input("기온 (°C)", value=20.0)

if st.button("예측하기"):
    pred = model.predict([[hour, temp]])
    st.success(f"예상 교통량: {int(pred[0]):,} 대")

