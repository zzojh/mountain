import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 선택
page = st.sidebar.selectbox("📌 페이지 선택", ["🌍 해수면 상승 시뮬레이터", "⚠️ 피해 설명"])

if page == "🌍 해수면 상승 시뮬레이터":
    st.title("🌊 해수면 상승 시뮬레이터")
    st.markdown("기후 변화로 인한 해수면 상승이 세계 도시에 미치는 영향을 시각화합니다.")

    data = [
        {"city": "뉴욕", "lat": 40.7128, "lon": -74.0060, "flood_threshold": 100},
        {"city": "런던", "lat": 51.5074, "lon": -0.1278, "flood_threshold": 80},
        {"city": "도쿄", "lat": 35.6762, "lon": 139.6503, "flood_threshold": 120},
        {"city": "시드니", "lat": -33.8688, "lon": 151.2093, "flood_threshold": 90},
        {"city": "뭄바이", "lat": 19.0760, "lon": 72.8777, "flood_threshold": 110},
        {"city": "상하이", "lat": 31.2304, "lon": 121.4737, "flood_threshold": 95},
        {"city": "방콕", "lat": 13.7563, "lon": 100.5018, "flood_threshold": 85},
        {"city": "로스앤젤레스", "lat": 34.0522, "lon": -118.2437, "flood_threshold": 105},
        {"city": "마이애미", "lat": 25.7617, "lon": -80.1918, "flood_threshold": 90},
        {"city": "리우데자네이루", "lat": -22.9068, "lon": -43.1729, "flood_threshold": 100},
        {"city": "케이프타운", "lat": -33.9249, "lon": 18.4241, "flood_threshold": 85},
        {"city": "싱가포르", "lat": 1.3521, "lon": 103.8198, "flood_threshold": 90},
        {"city": "바르셀로나", "lat": 41.3851, "lon": 2.1734, "flood_threshold": 95},
        {"city": "두바이", "lat": 25.276987, "lon": 55.296249, "flood_threshold": 100},
        {"city": "암스테르담", "lat": 52.3676, "lon": 4.9041, "flood_threshold": 80},
        {"city": "베니스", "lat": 45.4408, "lon": 12.3155, "flood_threshold": 70},
        {"city": "부에노스아이레스", "lat": -34.6037, "lon": -58.3816, "flood_threshold": 100},
        {"city": "이스탄불", "lat": 41.0082, "lon": 28.9784, "flood_threshold": 95},
        {"city": "밴쿠버", "lat": 49.2827, "lon": -123.1207, "flood_threshold": 90},
        {"city": "오사카", "lat": 34.6937, "lon": 135.5023, "flood_threshold": 110},
        {"city": "호치민", "lat": 10.7769, "lon": 106.7009, "flood_threshold": 85},
        {"city": "카라치", "lat": 24.8607, "lon": 67.0011, "flood_threshold": 95},
        {"city": "콜카타", "lat": 22.5726, "lon": 88.3639, "flood_threshold": 90},
        {"city": "하노이", "lat": 21.0285, "lon": 105.8542, "flood_threshold": 88},
        {"city": "자카르타", "lat": -6.2088, "lon": 106.8456, "flood_threshold": 70},
        {"city": "서울", "lat": 37.5665, "lon": 126.9780, "flood_threshold": 100},
        {"city": "부산", "lat": 35.1796, "lon": 129.0756, "flood_threshold": 95},
        {"city": "인천", "lat": 37.4563, "lon": 126.7052, "flood_threshold": 92},
        {"city": "포항", "lat": 36.0190, "lon": 129.3435, "flood_threshold": 88},
        {"city": "여수", "lat": 34.7604, "lon": 127.6622, "flood_threshold": 85}
    ]

    df = pd.DataFrame(data)

    temp = st.slider("🌡️ 지구 평균 온도 상승 (°C)", 0.0, 5.0, 1.0, 0.1)
    year = st.slider("📅 예상 연도", 2025, 2100, 2050, 5)
    rise_cm = temp * 25
    st.write(f"📈 예상 해수면 상승: **{rise_cm:.1f}cm** ({year}년 기준)")

    def get_risk(rise, threshold):
        if rise >= threshold:
            return "🔴 높음"
        elif rise >= threshold * 0.5:
            return "🟠 중간"
        else:
            return "🟢 낮음"

    df["위험도"] = df["flood_threshold"].apply(lambda x: get_risk(rise_cm, x))

    st.markdown("### ➕ 사용자 지정 도시 추가")
    with st.form("add_city_form"):
        city_name = st.text_input("도시 이름")
        city_lat = st.number_input("위도", format="%.6f")
        city_lon = st.number_input("경도", format="%.6f")
        city_threshold = st.number_input("침수 임계값 (cm)", min_value=1)
        add_button = st.form_submit_button("도시 추가")

    if add_button and city_name:
        new_risk = get_risk(rise_cm, city_threshold)
        df = pd.concat([df, pd.DataFrame([{
            "city": city_name,
            "lat": city_lat,
            "lon": city_lon,
            "flood_threshold": city_threshold,
            "위험도": new_risk
        }])], ignore_index=True)
        st.success(f"✅ '{city_name}'이(가) 추가되었습니다!")

    selected_city = st.selectbox("🗺️ 지도 중심 도시 선택", df["city"])
    center = df[df["city"] == selected_city][["lat", "lon"]].iloc[0].values.tolist()

    m = folium.Map(location=center, zoom_start=3)
    color_map = {"🔴 높음": "red", "🟠 중간": "orange", "🟢 낮음": "green"}

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            color=color_map[row["위험도"]],
            fill=True,
            fill_opacity=0.7,
            popup=f"{row['city']}<br>위험도: {row['위험도']}<br>임계값: {row['flood_threshold']}cm"
        ).add_to(m)

    st_folium(m, width=800, height=500)

    with st.expander("📊 침수 위험 도시 표 보기"):
        st.dataframe(df[["city", "위험도", "flood_threshold"]].rename(columns={
            "city": "도시", "flood_threshold": "임계값 (cm)"
        }))

# 피해 설명 페이지
elif page == "⚠️ 피해 설명":
    st.markdown("<h1 style='color:#d62728;'>⚠️ 해수면 상승 피해 설명</h1>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .impact-box {
        border-radius: 6px;
        padding: 10px 15px;
        margin-bottom: 15px;
        font-size: 16px;
        line-height: 1.6;
    }
    .low { background-color: #dff0d8; border-left: 6px solid #3c763d; }
    .moderate { background-color: #fcf8e3; border-left: 6px solid #8a6d3b; }
    .high { background-color: #f2dede; border-left: 6px solid #a94442; }
    </style>

    <div class="impact-box low">
    <b>📏 0~25cm 상승</b><br>
    - 저지대 소규모 침수 발생 가능<br>
    - 해안 생태계 변화 시작<br>
    - 일부 농작물 염해 피해 🌱
    </div>

    <div class="impact-box moderate">
    <b>📏 25~50cm 상승</b><br>
    - 섬 국가 침수 가시화 (예: 투발루)<br>
    - 저지대 인구 이주 발생<br>
    - 주요 도시 하수도 역류 위험 💦
    </div>

    <div class="impact-box moderate">
    <b>📏 50~100cm 상승</b><br>
    - 도시 인프라 침수 (항만, 철도 등)<br>
    - 기후 난민 급증<br>
    - 식수 오염과 염수 침투 문제 💧
    </div>

    <div class="impact-box high">
    <b>📏 100cm 이상 상승</b><br>
    - 해안선 대규모 침수<br>
    - 대규모 기후 이주자 발생<br>
    - 생태계 및 경제 시스템 붕괴 위험 🌍
    </div>
    """, unsafe_allow_html=True)

