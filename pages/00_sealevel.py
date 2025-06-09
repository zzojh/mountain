import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

def simulator_page():
    st.title("🌊 해수면 상승 & 침수 위험 시뮬레이터 🐳")

    # 주요 도시 및 피해 취약 지역 (더 많이 추가)
    data = [
        {"city": "뉴욕 🗽", "lat": 40.7128, "lon": -74.0060, "flood_threshold": 100},
        {"city": "런던 🎡", "lat": 51.5074, "lon": -0.1278, "flood_threshold": 80},
        {"city": "도쿄 🗼", "lat": 35.6762, "lon": 139.6503, "flood_threshold": 120},
        {"city": "투발루 🏝️", "lat": -7.1095, "lon": 179.1943, "flood_threshold": 30},
        {"city": "모가디슈 (소말리아) 🏝️", "lat": 2.0469, "lon": 45.3182, "flood_threshold": 70},
        {"city": "라고스 (나이지리아) 🌊", "lat": 6.5244, "lon": 3.3792, "flood_threshold": 75},
        {"city": "알렉산드리아 (이집트) 🐪", "lat": 31.2001, "lon": 29.9187, "flood_threshold": 65},
        {"city": "방콕 🌴", "lat": 13.7563, "lon": 100.5018, "flood_threshold": 90},
        {"city": "상하이 🏙️", "lat": 31.2304, "lon": 121.4737, "flood_threshold": 110},
        {"city": "마이애미 🏖️", "lat": 25.7617, "lon": -80.1918, "flood_threshold": 85},
        {"city": "뭄바이 🕌", "lat": 19.0760, "lon": 72.8777, "flood_threshold": 95},
        {"city": "시드니 🐨", "lat": -33.8688, "lon": 151.2093, "flood_threshold": 105},
        {"city": "카이로 🏜️", "lat": 30.0444, "lon": 31.2357, "flood_threshold": 70},
        {"city": "다카 (방글라데시) 🌾", "lat": 23.8103, "lon": 90.4125, "flood_threshold": 60},
        {"city": "싱가포르 🌇", "lat": 1.3521, "lon": 103.8198, "flood_threshold": 75},
        {"city": "리우데자네이루 🌞", "lat": -22.9068, "lon": -43.1729, "flood_threshold": 80},
        {"city": "암스테르담 🚲", "lat": 52.3676, "lon": 4.9041, "flood_threshold": 90},
        {"city": "마닐라 🌊", "lat": 14.5995, "lon": 120.9842, "flood_threshold": 65},
        {"city": "다윈 (호주) 🐊", "lat": -12.4634, "lon": 130.8456, "flood_threshold": 55},
        {"city": "호놀룰루 🏝️", "lat": 21.3069, "lon": -157.8583, "flood_threshold": 75},
        # 추가 도시들
        {"city": "발리 (인도네시아) 🌴", "lat": -8.3405, "lon": 115.0920, "flood_threshold": 50},
        {"city": "제네바 (스위스) 🏔️", "lat": 46.2044, "lon": 6.1432, "flood_threshold": 95},
        {"city": "부에노스아이레스 (아르헨티나) 🎭", "lat": -34.6037, "lon": -58.3816, "flood_threshold": 85},
        {"city": "케이프타운 (남아공) 🌅", "lat": -33.9249, "lon": 18.4241, "flood_threshold": 70},
        {"city": "오사카 (일본) 🏯", "lat": 34.6937, "lon": 135.5023, "flood_threshold": 110},
        {"city": "방콕 (태국) 🌾", "lat": 13.7563, "lon": 100.5018, "flood_threshold": 90},
    ]

    df = pd.DataFrame(data)

    temp_rise = st.slider("🌡️ 지구 평균 온도 상승 (℃)", 0.0, 5.0, 1.0, 0.1)

    sea_level_rise = temp_rise * 25  # cm 단위

    st.markdown(f"### 🌊 예상 해수면 상승: {sea_level_rise:.1f} cm")

    def risk_level(sea_level, threshold):
        if sea_level >= threshold:
            return "높음 🔴"
        elif sea_level >= threshold * 0.5:
            return "중간 🟠"
        else:
            return "낮음 🟢"

    df['위험도'] = df['flood_threshold'].apply(lambda x: risk_level(sea_level_rise, x))

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

    with st.expander("📋 위험도별 도시 목록 보기/숨기기"):
        st.dataframe(df[['city', '위험도', 'flood_threshold']].rename(columns={
            'city': '도시',
            'flood_threshold': '침수 임계 높이 (cm)'
        }))

    risk_summary = df['위험도'].value_counts().reindex(['높음 🔴','중간 🟠','낮음 🟢']).fillna(0).astype(int)
    st.markdown("### 📝 위험도 요약")
    st.write(f"🔴 높음: {risk_summary['높음 🔴']}개 도시, 🟠 중간: {risk_summary['중간 🟠']}개 도시, 🟢 낮음: {risk_summary['낮음 🟢']}개 도시")

def impact_explanation_page():
    st.title("⚠️ 해수면 상승에 따른 피해 정도 상세 설명")

    st.markdown("""
    <style>
    .section-title {
        color: #1f77b4;  /* 파란색 */
        font-weight: bold;
        font-size: 22px;
        margin-top: 20px;
        margin-bottom: 8px;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 4px;
    }
    </style>

    <div class="section-title">해수면 상승과 관련된 피해 규모와 영향 🌍</div>
    <p>
    <b>0~25cm 상승</b><br>
    - 저지대 침수 위험 증가로 농업용지 및 주택 피해 발생<br>
    - 해안 습지 및 연안 생태계 변화 시작, 일부 어종 서식지 위협<br>
    - 인구 밀집 저지대 소도시에서 국지적 침수 발생 가능성 🏡
    </p>

    <p>
    <b>25~50cm 상승</b><br>
    - 섬나라(투발루, 몰디브) 및 저지대 해안 도시 침수 시작<br>
    - 해안 방파제와 하수도 시스템 과부하로 인한 생활 불편 증가<br>
    - 일부 농업 지역 염수 침투로 농작물 피해 심화 🚜
    </p>

    <p>
    <b>50~100cm 상승</b><br>
    - 대도시 주요 인프라(공항, 항만, 도로) 침수 위험 급증<br>
    - 대규모 인구 이주 및 난민 문제 발생 가능성<br>
    - 담수자원 오염 및 식수 공급에 심각한 위협 발생 💧
    </p>

    <p>
    <b>100cm 이상 상승</b><br>
    - 광범위한 해안선 침수, 국가 경제 및 사회 전반에 큰 타격<br>
    - 생태계 파괴 및 기후 난민 폭증으로 인한 사회적 갈등 심화<br>
    - 지속 가능한 적응 정책 및 재난 대비 없이는 심각한 인명 피해 발생 가능 🌊
    </p>

    <hr>

    <div class="section-title">사례 연구</div>
    <ul>
    <li><b>투발루</b>: 해수면 상승 30cm 정도면 섬 대부분 침수 위협, 이미 이주 시작됨</li>
    <li><b>방글라데시 다카</b>: 연간 홍수 피해 빈도가 증가, 해안 염수 침투 심각</li>
    <li><b>뉴욕</b>: 허리케인 및 폭우 시 침수 피해 급증, 방재 시설 확충 중</li>
    <li><b>암스테르담</b>: 해수면 상승 대비 치수 시스템 매우 발달, 성공적인 적응 사례</li>
    </ul>

    <hr>

    <div class="section-title">해수면 상승 대응 전략</div>
    <ul>
    <li>연안 방파제 및 홍수 방지 인프라 구축</li>
    <li>지속 가능한 도시 계획과 이주 정책 마련</li>
    <li>기후 변화 완화를 위한 글로벌 협력 강화</li>
    <li>생태계 복원 및 자연 기반 해법 적극 도입</li>
    </ul>

    <hr>

    <p>🌱 <b>기후 변화 문제는 우리 모두의 문제입니다. 함께 이해하고 행동하는 것이 중요해요!</b></p>
    """, unsafe_allow_html=True)


def main():
    st.title("🌍 해수면 상승 시뮬레이터 & 피해 설명")

    page = st.selectbox("🔎 페이지 선택", ("시뮬레이터", "피해 설명"))

    if page == "시뮬레이터":
        simulator_page()
    elif page == "피해 설명":
        impact_explanation_page()

if __name__ == "__main__":
    main()
