import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 스타일 함수
def styled_title(text):
    st.markdown(f"<h2 style='color:#1e3a8a; text-decoration: underline; margin-bottom:5px;'>{text}</h2>", unsafe_allow_html=True)

def colored_text(text, color, size="16px", bold=False, underline=False):
    weight = "bold" if bold else "normal"
    under = "underline" if underline else "none"
    st.markdown(
        f"<p style='color:{color}; font-size:{size}; font-weight:{weight}; text-decoration:{under}; margin-bottom:5px;'>{text}</p>",
        unsafe_allow_html=True
    )

def white_text(text, size="16px"):
    st.markdown(f"<p style='color:#ffffff; font-size:{size}; margin-bottom:5px;'>{text}</p>", unsafe_allow_html=True)

# 도시 데이터에 국가 컬럼 추가
data = [
    {"city": "뉴욕", "country":"미국", "lat": 40.7128, "lon": -74.0060, "flood_threshold": 100},
    {"city": "런던", "country":"영국", "lat": 51.5074, "lon": -0.1278, "flood_threshold": 80},
    {"city": "도쿄", "country":"일본", "lat": 35.6762, "lon": 139.6503, "flood_threshold": 120},
    {"city": "시드니", "country":"호주", "lat": -33.8688, "lon": 151.2093, "flood_threshold": 90},
    {"city": "뭄바이", "country":"인도", "lat": 19.0760, "lon": 72.8777, "flood_threshold": 110},
    {"city": "상하이", "country":"중국", "lat": 31.2304, "lon": 121.4737, "flood_threshold": 95},
    {"city": "방콕", "country":"태국", "lat": 13.7563, "lon": 100.5018, "flood_threshold": 85},
    {"city": "로스앤젤레스", "country":"미국", "lat": 34.0522, "lon": -118.2437, "flood_threshold": 105},
    {"city": "마이애미", "country":"미국", "lat": 25.7617, "lon": -80.1918, "flood_threshold": 90},
    {"city": "리우데자네이루", "country":"브라질", "lat": -22.9068, "lon": -43.1729, "flood_threshold": 100},
    {"city": "케이프타운", "country":"남아프리카공화국", "lat": -33.9249, "lon": 18.4241, "flood_threshold": 85},
    {"city": "싱가포르", "country":"싱가포르", "lat": 1.3521, "lon": 103.8198, "flood_threshold": 90},
    {"city": "바르셀로나", "country":"스페인", "lat": 41.3851, "lon": 2.1734, "flood_threshold": 95},
    {"city": "두바이", "country":"아랍에미리트", "lat": 25.276987, "lon": 55.296249, "flood_threshold": 100},
    {"city": "암스테르담", "country":"네덜란드", "lat": 52.3676, "lon": 4.9041, "flood_threshold": 80},
    {"city": "베니스", "country":"이탈리아", "lat": 45.4408, "lon": 12.3155, "flood_threshold": 70},
    {"city": "부에노스아이레스", "country":"아르헨티나", "lat": -34.6037, "lon": -58.3816, "flood_threshold": 100},
    {"city": "이스탄불", "country":"터키", "lat": 41.0082, "lon": 28.9784, "flood_threshold": 95},
    {"city": "밴쿠버", "country":"캐나다", "lat": 49.2827, "lon": -123.1207, "flood_threshold": 90},
    {"city": "오사카", "country":"일본", "lat": 34.6937, "lon": 135.5023, "flood_threshold": 110},
    {"city": "호치민", "country":"베트남", "lat": 10.7769, "lon": 106.7009, "flood_threshold": 85},
    {"city": "카라치", "country":"파키스탄", "lat": 24.8607, "lon": 67.0011, "flood_threshold": 95},
    {"city": "콜카타", "country":"인도", "lat": 22.5726, "lon": 88.3639, "flood_threshold": 90},
    {"city": "하노이", "country":"베트남", "lat": 21.0285, "lon": 105.8542, "flood_threshold": 88},
    {"city": "자카르타", "country":"인도네시아", "lat": -6.2088, "lon": 106.8456, "flood_threshold": 70},
    {"city": "서울", "country":"한국", "lat": 37.5665, "lon": 126.9780, "flood_threshold": 100},
    {"city": "부산", "country":"한국", "lat": 35.1796, "lon": 129.0756, "flood_threshold": 95},
    {"city": "인천", "country":"한국", "lat": 37.4563, "lon": 126.7052, "flood_threshold": 92},
    {"city": "포항", "country":"한국", "lat": 36.0190, "lon": 129.3435, "flood_threshold": 88},
    {"city": "여수", "country":"한국", "lat": 34.7604, "lon": 127.6622, "flood_threshold": 85}
]

df = pd.DataFrame(data)

# 페이지 선택용 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = "home"

# 페이지 선택 버튼 UI
col1, col2 = st.columns(2)
with col1:
    if st.button("🌍 해수면 상승 시뮬레이터"):
        st.session_state.page = "simulator"
with col2:
    if st.button("⚠️ 피해 설명"):
        st.session_state.page = "damage"

if st.session_state.page == "simulator":
    st.title("🌊 해수면 상승 시뮬레이터")
    st.write("기후 변화로 인한 해수면 상승이 세계 도시에 미치는 영향을 시각화합니다.")

    # 국가 선택 추가
    countries = sorted(df['country'].unique())
    selected_country = st.selectbox("국가 선택", countries)
    df_country = df[df["country"] == selected_country]

    # 도시 선택 (국가 필터 후)
    city_list = df_country["city"].tolist()
    if city_list:
        selected_city = st.selectbox("도시 선택", city_list)
    else:
        st.write("해당 국가에 등록된 도시가 없습니다.")
        selected_city = None

    temp = st.slider("🌡️ 지구 평균 온도 상승 (°C)", 0.0, 5.0, 1.0, 0.1)
    year = st.slider("📅 예상 연도", 2025, 2100, 2050, 5)
    rise_cm = temp * 25
    st.write(f"📈 예상 해수면 상승: **{rise_cm:.1f}cm** ({year}년 기준)")

    def get_risk(rise, threshold):
        if rise >= threshold:
            return "높음"
        elif rise >= threshold * 0.5:
            return "중간"
        else:
            return "낮음"

    df_country["위험도"] = df_country["flood_threshold"].apply(lambda x: get_risk(rise_cm, x))

    if selected_city:
        center = df_country[df_country["city"] == selected_city][["lat", "lon"]].iloc[0].values.tolist()
    else:
        center = [20,0]  # 기본 위치

    m = folium.Map(location=center, zoom_start=4)

    color_map = {
        "높음": "#e63946",
        "중간": "#f4a261",
        "낮음": "#2a9d8f"
    }

    for _, row in df_country.iterrows():
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
        st.dataframe(df_country[["city", "위험도", "flood_threshold"]].rename(columns={
            "city": "도시", "flood_threshold": "임계값 (cm)"
        }))

elif st.session_state.page == "damage":
    st.title("⚠️ 해수면 상승 피해 설명")

    styled_title("0 ~ 25cm 상승 (위험도: 낮음)")
    white_text("● 저지대 소규모 침수 발생 가능")
    white_text("● 해안 생태계 변화 시작")
    white_text("● 일부 농작물 염해 피해 🌱")

    styled_title("25 ~ 50cm 상승 (위험도: 중간)")
    white_text("● 섬 국가 침수 가시화 (예: 투발루)")
    white_text("● 저지대 인구 이주 발생")
    white_text("● 주요 도시 하수도 역류 위험 💦")

    styled_title("50 ~ 100cm 상승 (위험도: 높음)")
    white_text("● 도시 인프라 침수 (항만, 철도 등)")
    white_text("● 기후 난민 급증")
    white_text("● 식수 오염과 염수 침투 문제 💧")

    styled_title("100cm 이상 상승 (위험도: 매우 높음)")
    white_text("● 해안선 대규모 침수")
    white_text("● 대규모 기후 이주자 발생")
    white_text("● 생태계 및 경제 시스템 붕괴 위험 🌍")

    st.markdown("---")

    styled_title("🌍 실제 피해 사례")
    colored_text("1. 필리핀 루손섬 어촌 공동체: 태풍 하이옌 이후 해수면 상승과 어획량 감소로 피해 발생. 맹그로브 복원과 생계 다각화로 대응 중.", "#1e3a8a", size="15px", bold=True)
    st.markdown("[관련 기사 보기](https://time.com/7289533/philippines-fishing-communities-rising-water/)", unsafe_allow_html=True)

    colored_text("2. 멕시코 엘 보스케 마을: 해수면 상승과 폭풍으로 주민 다수가 이주, 정부 지원 지연 속 자력 재건 시도.", "#1e3a8a", size="15px", bold=True)
    st.markdown("[관련 기사 보기](https://apnews.com/article/ec3aabaa42157f172e1b27f489104641)", unsafe_allow_html=True)

    colored_text("3. 투발루 해안 적응 프로젝트 (TCAP): 해안 보호 구조물, 맹그로브 복원, 주민 역량 강화로 해수면 상승 대응.", "#1e3a8a", size="15px", bold=True)
    st.markdown("[관련 위키피디아](https://en.wikipedia.org/wiki/Tuvalu_Coastal_Adaptation_Project)", unsafe_allow_html=True)

    st.markdown("---")

    styled_title("🛠️ 대응 및 해결 방안")
    colored_text("• 자연 기반 해결책: 맹그로브 숲, 염습지 복원 등 생태계 보호 및 해안선 안정화", "#1e3a8a", size="15px")
    colored_text("• 해안 방어 구조물 구축: 제방, 방조제, 해안 방파제 등 인프라 강화", "#1e3a8a", size="15px")
    colored_text("• 지역 이주 및 재정착: 위험 지역 주민의 안전한 이주 및 지원 정책 마련", "#1e3a8a", size="15px")
    colored_text("• 지속 가능한 도시 개발: 스펀지 도시 개념 도입으로 자연 수자원 관리 및 홍수 완화", "#1e3a8a", size="15px")
