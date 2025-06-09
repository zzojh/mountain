import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 주요 해안 도시 데이터 예시 (위도, 경도, 도시, 기준 해수면 높이, 임계 침수 높이(cm))
data = [
    {"city": "뉴욕", "lat": 40.7128, "lon": -74.0060, "base_level": 0, "flood_threshold": 100},
    {"city": "런던", "lat": 51.5074, "lon": -0.1278, "base_level": 0, "flood_threshold": 80},
    {"city": "도쿄", "lat": 35.6762, "lon": 139.6503, "base_level": 0, "flood_threshold": 120},
    {"city": "시드니", "lat": -33.8688, "lon": 151.2093, "base_level": 0, "flood_threshold": 90},
    {"city": "뭄바이", "lat": 19.0760, "lon": 72.8777, "base_level": 0, "flood_threshold": 110},
    {"city": "상하이", "lat": 31.2304, "lon": 121.4737, "base_level": 0, "flood_threshold": 95},
    {"city": "방콕", "lat": 13.7563, "lon": 100.5018, "base_level": 0, "flood_threshold": 85},
]

df = pd.DataFrame(data)

st.title("🌍 지구 온도 상승에 따른 해수면 상승 & 침수 위험 시뮬레이터")

# 2. 지구 온도 상승 입력 (0~5도)
temp_rise = st.slider("지구 평균 온도 상승 (℃)", 0.0, 5.0, 1.0, 0.1)

# 3. 온도 상승 -> 해수면 상승 (cm)
sea_level_rise = temp_rise * 25  # 1도 당 25cm 상승 가정
st.markdown(f"### 예상 해수면 상승: {sea_level_rise:.1f} cm")

# 4. 위험도 분류 (해수면 상승이 임계치보다 크면 위험)
def risk_level(sea_level, threshold):
    if sea_level >= threshold:
        return "높음"
    elif sea_level >= threshold * 0.5:
        return "중간"
    else:
        return "낮음"

df['risk'] = df['flood_threshold'].apply(lambda x: risk_level(sea_level_rise, x))

# 5. 지도 생성 (세계 중심)
m = folium.Map(location=[20,0], zoom_start=2)

# 위험도별 색깔
risk_colors = {
    "높음": "red",
    "중간": "orange",
    "낮음": "green"
}

# 6. 지도에 마커 표시
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=10,
        color=risk_colors[row['risk']],
        fill=True,
        fill_opacity=0.7,
        popup=f"{row['city']} - 위험도: {row['risk']} (임계치 {row['flood_threshold']}cm)"
    ).add_to(m)

st_folium(m, width=800, height=500)

# 7. 위험도별 도시 정리 표
st.markdown("### 위험도별 도시 목록 및 예상 침수 위험 정보")

st.dataframe(df[['city', 'risk', 'flood_threshold']].rename(columns={
    'city': '도시',
    'risk': '위험도',
    'flood_threshold': '침수 임계 높이(cm)'
}))

# 8. 위험도 요약
risk_summary = df['risk'].value_counts().reindex(['높음','중간','낮음']).fillna(0).astype(int)
st.markdown("### 위험도 요약")
st.write(f"높음: {risk_summary['높음']}개 도시, 중간: {risk_summary['중간']}개 도시, 낮음: {risk_summary['낮음']}개 도시")
