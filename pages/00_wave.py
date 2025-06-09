import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 🌎 해안 도시 데이터 (20개 이상)
data = [
    {"city": "뉴욕 🗽", "lat": 40.7128, "lon": -74.0060, "flood_threshold": 100},
    {"city": "런던 🎡", "lat": 51.5074, "lon": -0.1278, "flood_threshold": 80},
    {"city": "도쿄 🗼", "lat": 35.6762, "lon": 139.6503, "flood_threshold": 120},
    {"city": "시드니 🐨", "lat": -33.8688, "lon": 151.2093, "flood_threshold": 90},
    {"city": "뭄바이 🕌", "lat": 19.0760, "lon": 72.8777, "flood_threshold": 110},
    {"city": "상하이 🐉", "lat": 31.2304, "lon": 121.4737, "flood_threshold": 95},
    {"city": "방콕 🛕", "lat": 13.7563, "lon": 100.5018, "flood_threshold": 85},
    {"city": "로스앤젤레스 🎬", "lat": 34.0522, "lon": -118.2437, "flood_threshold": 105},
    {"city": "마이애미 🏝️", "lat": 25.7617, "lon": -80.1918, "flood_threshold": 90},
    {"city": "리우데자네이루 🎉", "lat": -22.9068, "lon": -43.1729, "flood_threshold": 100},
    {"city": "케이프타운 🦁", "lat": -33.9249, "lon": 18.4241, "flood_threshold": 85},
    {"city": "싱가포르 🦀", "lat": 1.3521, "lon": 103.8198, "flood_threshold": 90},
    {"city": "바르셀로나 🏰", "lat": 41.3851, "lon": 2.1734, "flood_threshold": 95},
    {"city": "두바이 🏙️", "lat": 25.276987, "lon": 55.296249, "flood_threshold": 100},
    {"city": "암스테르담 🚲", "lat": 52.3676, "lon": 4.9041, "flood_threshold": 80},
    {"city": "베니스 🛶", "lat": 45.4408, "lon": 12.3155, "flood_threshold": 70},
    {"city": "부에노스아이레스 🎭", "lat": -34.6037, "lon": -58.3816, "flood_threshold": 100},
    {"city": "이스탄불 🕌", "lat": 41.0082, "lon": 28.9784, "flood_threshold": 95},
    {"city": "밴쿠버 🍁", "lat": 49.2827, "lon": -123.1207, "flood_threshold": 90},
    {"city": "오사카 🍣", "lat": 34.6937, "lon": 135.5023, "flood_threshold": 110},
]

df = pd.DataFrame(data)

st.title("🌍 지구 온도 상승에 따른 해수면 상승 & 침수 위험 시뮬레이터 🐳")

# 온도 상승 입력
temp_rise = st.slider("🌡️ 지구 평균 온도 상승 (℃)", 0.0, 5.0, 1.0, 0.1)

# 해수면 상승 계산 (1℃당 25cm 상승 가정)
sea_level_rise = temp_rise * 25  
st.markdown(f"### 🌊 예상 해수면 상승: {sea_level_rise:.1f} cm")

# 위험도 판단 함수
def risk_level(sea_level, threshold):
    if sea_level >= threshold:
        return "높음 🔴"
    elif sea_level >= threshold * 0.5:
        return "중간 🟠"
    else:
        return "낮음 🟢"

df['위험도'] = df['flood_threshold'].apply(lambda x: risk_level(sea_level_rise, x))

# 지도 생성
m = folium.Map(location=[20,0], zoom_start=2)

risk_colors = {
    "높음 🔴": "red",
    "중간 🟠": "orange",
    "낮음 🟢": "green"
}

for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=10,
        color=risk_colors[row['위험도']],
        fill=True,
        fill_opacity=0.7,
        popup=f"{row['city']} - 위험도: {row['위험도']} (임계치 {row['flood_threshold']}cm)"
    ).add_to(m)

st_folium(m, width=800, height=500)

# 토글박스로 표 보여주기
with st.expander("📋 위험도별 도시 목록 보기/숨기기"):
    st.dataframe(df[['city', '위험도', 'flood_threshold']].rename(columns={
        'city': '도시',
        'flood_threshold': '침수 임계 높이 (cm)'
    }))

# 위험도 요약
risk_summary = df['위험도'].value_counts().reindex(['높음 🔴','중간 🟠','낮음 🟢']).fillna(0).astype(int)
st.markdown("### 📝 위험도 요약")
st.write(f"🔴 높음: {risk_summary['높음 🔴']}개 도시, 🟠 중간: {risk_summary['중간 🟠']}개 도시, 🟢 낮음: {risk_summary['낮음 🟢']}개 도시")
