import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 샘플 도시 데이터: 위도, 경도, 도시 이름
cities = pd.DataFrame({
    'city': ['서울', '부산', '인천', '광주', '대구'],
    'lat': [37.5665, 35.1796, 37.4563, 35.1595, 35.8722],
    'lon': [126.9780, 129.0756, 126.7052, 126.8526, 128.6014]
})

st.title("🌊 해수면 상승 시뮬레이터")

sea_level_rise = st.slider("예상 해수면 상승 높이 (cm)", 0, 300, 50)

city = st.selectbox("분석할 도시 선택", cities['city'])

# 도시 좌표 가져오기
city_data = cities[cities['city'] == city].iloc[0]
lat, lon = city_data['lat'], city_data['lon']

# 지도 생성 (도시 중심)
m = folium.Map(location=[lat, lon], zoom_start=11)

# 해수면 상승 시 영향을 받는 가상의 범위 표시 (단순 원 형태)
# 해수면 상승이 클수록 침수 범위 증가(단순 가정)
radius = sea_level_rise * 20  # cm 단위를 확대해서 반경(m)로 사용

folium.Circle(
    location=[lat, lon],
    radius=radius,
    color='blue',
    fill=True,
    fill_opacity=0.3,
    popup=f"{city} 예상 침수 지역 (반경 {radius}m)"
).add_to(m)

st.markdown(f"### {city} 지역의 예상 침수 반경: 약 {radius} 미터")

# 지도 렌더링
st_folium(m, width=700, height=500)

st.markdown("""
---
### 참고
- 이 시뮬레이터는 실제 지형, 해안선 데이터, 해수면 상승 복잡성을 단순화한 모델입니다.
- 실제 침수 지역은 해안선, 지형, 방재시설 등에 따라 다릅니다.
- 향후 기후변화 시나리오별 상세 모델을 추가할 수 있습니다.
""")
