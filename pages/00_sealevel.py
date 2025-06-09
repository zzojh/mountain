import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 스타일 함수
def styled_title(text):
    st.markdown(f"<h2 style='color:#1e3a8a; text-decoration: underline; margin-bottom:5px;'>{text}</h2>", unsafe_allow_html=True)

def white_text(text, size="16px", bold=False):
    weight = "bold" if bold else "normal"
    st.markdown(f"<p style='color:#ffffff; font-size:{size}; font-weight:{weight}; margin-bottom:5px;'>{text}</p>", unsafe_allow_html=True)

# 도시 데이터 (예시)
data = [
    {"city": "뉴욕", "country":"미국", "lat": 40.7128, "lon": -74.0060, "flood_threshold": 100},
    {"city": "런던", "country":"영국", "lat": 51.5074, "lon": -0.1278, "flood_threshold": 80},
    {"city": "도쿄", "country":"일본", "lat": 35.6762, "lon": 139.6503, "flood_threshold": 120},
    {"city": "시드니", "country":"호주", "lat": -33.8688, "lon": 151.2093, "flood_threshold": 90},
    {"city": "마이애미", "country":"미국", "lat": 25.7617, "lon": -80.1918, "flood_threshold": 90},
    {"city": "방콕", "country":"태국", "lat": 13.7563, "lon": 100.5018, "flood_threshold": 85},
    {"city": "서울", "country":"한국", "lat": 37.5665, "lon": 126.9780, "flood_threshold": 100},
    {"city": "부산", "country":"한국", "lat": 35.1796, "lon": 129.0756, "flood_threshold": 95},
]

df = pd.DataFrame(data)

# 세션 상태 초기화
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

    # 온도 상승 및 연도 선택
    temp = st.slider("🌡️ 지구 평균 온도 상승 (°C)", 0.0, 5.0, 1.0, 0.1)
    year = st.slider("📅 예상 연도", 2025, 2100, 2050, 5)

    rise_cm = temp * 25
    st.write(f"📈 예상 해수면 상승: **{rise_cm:.1f}cm** ({year}년 기준)")

    # 위험도 계산
    def get_risk(rise, threshold):
        if rise >= threshold:
            return "높음"
        elif rise >= threshold * 0.5:
            return "중간"
        else:
            return "낮음"

    df["위험도"] = df["flood_threshold"].apply(lambda x: get_risk(rise_cm, x))

    # 지도 중심 세계 중앙
    center = [20, 0]
    m = folium.Map(location=center, zoom_start=2)

    # 색깔 맵 (파스텔톤)
    color_map = {
        "높음": "#F7A6B1",  # 연한 핑크
        "중간": "#B3D4F7",  # 연한 하늘색
        "낮음": "#CAB8F7"   # 연한 보라색
    }

    # 피해 예상 도시 모두 표시 (위험도별 색상)
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            color=color_map[row["위험도"]],
            fill=True,
            fill_opacity=0.6,
            popup=f"{row['city']} ({row['country']})<br>위험도: {row['위험도']}<br>임계값: {row['flood_threshold']}cm"
        ).add_to(m)

    # 사용자 도시 추가 (위도, 경도, 설명)
    st.markdown("---")
    styled_title("➕ 사용자 지정 도시 추가")

    user_lat = st.number_input("위도 (Latitude)", min_value=-90.0, max_value=90.0, value=37.5665, format="%.6f")
    user_lon = st.number_input("경도 (Longitude)", min_value=-180.0, max_value=180.0, value=126.9780, format="%.6f")
    user_desc = st.text_input("도시 이름 또는 위치 설명")

    if st.button("➕ 지도에 추가"):
        folium.Marker(
            location=[user_lat, user_lon],
            popup=user_desc if user_desc else "사용자 지정 위치",
            icon=folium.Icon(color="blue", icon="map-marker", prefix='fa')
        ).add_to(m)
        st.success("지도에 위치가 추가되었습니다!")

    st_folium(m, width=800, height=500)

    # 위험도 데이터 테이블 토글(expander)
    with st.expander("📊 침수 위험 도시 표 보기"):
        st.dataframe(df[["city", "country", "위험도", "flood_threshold"]].rename(columns={
            "city": "도시",
            "country": "국가",
            "flood_threshold": "임계값 (cm)"
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
    white_text("1. 필리핀 루손섬 어촌 공동체: 태풍 하이옌 이후 해수면 상승과 어획량 감소로 피해 발생. 맹그로브 복원과 생계 다각화로 대응 중.")
    st.markdown("[관련 기사 보기](https://time.com/7289533/philippines-fishing-communities-rising-water/)", unsafe_allow_html=True)

    white_text("2. 멕시코 엘 보스케 마을: 해수면 상승과 폭풍으로 주민 다수가 이주, 정부 지원 지연 속 자력 재건 시도.")
    st.markdown("[관련 기사 보기](https://apnews.com/article/ec3aabaa42157f172e1b27f489104641)", unsafe_allow_html=True)

    white_text("3. 투발루 해안 적응 프로젝트 (TCAP): 해안 보호 구조물, 맹그로브 복원, 주민 역량 강화로 해수면 상승 대응.")
    st.markdown("[관련 위키피디아](https://en.wikipedia.org/wiki/Tuvalu_Coastal_Adaptation_Project)", unsafe_allow_html=True)

    st.markdown("---")

    styled_title("🛠️ 대응 및 해결 방안")
    white_text("• 자연 기반 해결책: 맹그로브 숲, 염습지 복원 등 생태계 보호 및 해안선 안정화")
    white_text("• 해안 방어 구조물 구축: 제방, 방조제, 해안 방파제 등 인프라 강화")
    white_text("• 지역 이주 및 재정착: 위험 지역 주민의 안전한 이주 및 지원 정책 마련")
    white_text("• 지속 가능한 도시 개발: 스펀지 도시 개념 도입으로 자연 수자원 관리 및 홍수 완화")

