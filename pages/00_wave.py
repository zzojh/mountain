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
    st.title("⚠️ 해수면 상승에 따른 피해 정도 설명")

    st.markdown("""
    ### 해수면 상승 구간별 피해 예시

    - **0~25cm 상승**  
      대부분 저지대 침수 위험 증가, 농경지 피해 발생 가능성, 해안가 생태계 변화 시작 🌱

    - **25~50cm 상승**  
      소규모 섬과 저지대 해안 도시 침수, 해안가 인프라 피해, 주민 이주 증가 가능성 🏚️

    - **50~100cm 상승**  
      대규모 도시 침수 위험, 주요 항만과 공항 피해, 농업 및 식수 공급에 심각한 영향 🍽️

    - **100cm 이상 상승**  
      광범위한 인구 이동 및 난민 발생, 국가 경제 큰 타격, 생태계 파괴 및 장기적 피해 🌊

    ---

    ### 참고  
    - 피해 규모는 도시별 지형, 방재시설, 정책에 따라 차이가 큽니다.  
    - 지속적인 기후 변화 대응과 적응 전략 수립이 매우 중요합니다.
    """)

def main():
    st.sidebar.title("메뉴")
    page = st.sidebar.radio("페이지 선택", ("시뮬레이터", "피해 설명"))

    if page == "시뮬레이터":
        simulator_page()
    elif page == "피해 설명":
        impact_explanation_page()

if __name__ == "__main__":
    main()
