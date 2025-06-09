import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 선택 버튼
col1, col2 = st.columns(2)
with col1:
    sim_btn = st.button("🌍 해수면 상승 시뮬레이터")
with col2:
    desc_btn = st.button("⚠️ 피해 설명")

# 기본 값
page = "🌍 해수면 상승 시뮬레이터" if sim_btn or (not sim_btn and not desc_btn) else "⚠️ 피해 설명"

# 시뮬레이터 페이지
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
    def render_impact_section(title, color_bg, color_border, content_lines):
    st.markdown(
        f"""
        <div style="
            background-color: {color_bg};
            border-left: 6px solid {color_border};
            border-radius: 8px;
            padding: 15px 20px;
            margin-bottom: 20px;
            color: black;
            font-size: 16px;
            line-height: 1.5;
            ">
            <strong style="font-size:18px;">{title}</strong><br>
            {"<br>".join(content_lines)}
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("⚠️ 해수면 상승 피해 설명")

# 파스텔 톤 색상 예시
render_impact_section(
    "📏 0~25cm 상승 (위험도: 낮음)",
    "#f9e6f9",  # 파스텔 핑크
    "#d18dc6",
    [
        "- 저지대 소규모 침수 발생 가능",
        "- 해안 생태계 변화 시작",
        "- 일부 농작물 염해 피해 🌱"
    ]
)

render_impact_section(
    "📏 25~50cm 상승 (위험도: 중간)",
    "#d0f0fd",  # 파스텔 하늘색
    "#5a9bd4",
    [
        "- 섬 국가 침수 가시화 (예: 투발루)",
        "- 저지대 인구 이주 발생",
        "- 주요 도시 하수도 역류 위험 💦"
    ]
)

render_impact_section(
    "📏 50~100cm 상승 (위험도: 높음)",
    "#e6d7f8",  # 파스텔 연보라색
    "#a085d9",
    [
        "- 도시 인프라 침수 (항만, 철도 등)",
        "- 기후 난민 급증",
        "- 식수 오염과 염수 침투 문제 💧"
    ]
)

render_impact_section(
    "📏 100cm 이상 상승 (위험도: 매우 높음)",
    "#ffd7e8",  # 연핑크색
    "#e085a6",
    [
        "- 해안선 대규모 침수",
        "- 대규모 기후 이주자 발생",
        "- 생태계 및 경제 시스템 붕괴 위험 🌍"
    ]
)

st.markdown("---")

st.header("🌍 실제 피해 사례")

st.markdown(
    """
    <div style="background:#e6f2ff; border-left: 6px solid #7fb3ff; border-radius:8px; padding:15px; margin-bottom:20px;">
    <strong>1. 필리핀 루손섬 어촌 공동체</strong><br>
    루손섬 어촌 지역은 태풍 하이옌 이후 해수면 상승과 어획량 감소로 큰 피해를 입었습니다. 맹그로브 복원과 지속 가능한 생계 다각화로 대응 중입니다.<br>
    <a href="https://time.com/7289533/philippines-fishing-communities-rising-water/" target="_blank">관련 기사 보기</a>
    </div>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <div style="background:#e6f2ff; border-left: 6px solid #7fb3ff; border-radius:8px; padding:15px; margin-bottom:20px;">
    <strong>2. 멕시코 엘 보스케 마을</strong><br>
    해수면 상승과 폭풍으로 인해 주민 다수가 이주했으며, 정부 지원 지연 속 자력 재건을 시도하고 있습니다.<br>
    <a href="https://apnews.com/article/ec3aabaa42157f172e1b27f489104641" target="_blank">관련 기사 보기</a>
    </div>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <div style="background:#e6f2ff; border-left: 6px solid #7fb3ff; border-radius:8px; padding:15px; margin-bottom:20px;">
    <strong>3. 투발루 해안 적응 프로젝트 (TCAP)</strong><br>
    해안 보호 구조물과 맹그로브 복원, 주민 역량 강화를 통해 해수면 상승에 대응하고 있습니다.<br>
    <a href="https://en.wikipedia.org/wiki/Tuvalu_Coastal_Adaptation_Project" target="_blank">관련 위키피디아</a>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("---")

st.header("🛠️ 대응 및 해결 방안")

st.markdown(
    """
    <ul>
        <li><strong>자연 기반 해결책:</strong> 맹그로브 숲, 염습지 복원 등을 통한 생태계 보호 및 해안선 안정화</li>
        <li><strong>해안 방어 구조물 구축:</strong> 제방, 방조제, 해안 방파제 등 인프라 강화</li>
        <li><strong>지역 이주 및 재정착:</strong> 위험 지역 주민의 안전한 이주 및 지원 정책 마련</li>
        <li><strong>지속 가능한 도시 개발:</strong> 스펀지 도시 개념 도입으로 자연 수자원 관리 및 홍수 완화</li>
    </ul>
    """,
    unsafe_allow_html=True
)
