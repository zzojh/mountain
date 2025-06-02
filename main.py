import streamlit as st

import time

st.title("🌟 MBTI 진로 추천기 🌟")

mbti_options = [
    "INTJ 🧠", "INTP 🤯", "ENTJ 👑", "ENTP 🧪",
    "INFJ 🌌", "INFP 🌸", "ENFJ 🎤", "ENFP 🌈",
    "ISTJ 🗂️", "ISFJ 🫶", "ESTJ 🧱", "ESFJ 🤝",
    "ISTP 🔧", "ISFP 🎨", "ESTP 🏎️", "ESFP 🎉"
]

mbti_choice = st.selectbox("👇 당신의 MBTI를 선택하세요!", mbti_options)

mbti_jobs = {
    "INTJ 🧠": ["데이터 사이언티스트 📊", "전략 컨설턴트 🧩", "AI 연구원 🤖"],
    "INTP 🤯": ["이론 물리학자 ⚛️", "프로덕트 디자이너 🛠️", "프로그래머 👨‍💻"],
    # 나머지는 동일...
}

if st.button("추천 직업 보기 🎬"):
    curtain = st.empty()
    result = st.empty()

    # Step 1: 커튼 닫힌 상태(흑색 박스 2개)
    curtain.markdown("""
    <div style="display:flex; justify-content: space-between; margin-bottom:20px;">
        <div style="background:#c71585; width:45%; height:150px; border-radius: 10px;"></div>
        <div style="background:#c71585; width:45%; height:150px; border-radius: 10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(1.5)

    # Step 2: 커튼 열림 (박스 사라지고 결과 표시)
    curtain.empty()

    jobs = mbti_jobs.get(mbti_choice, [])
    jobs_html = "<ul>"
    for job in jobs:
        jobs_html += f"<li>🎯 {job}</li>"
    jobs_html += "</ul>"

    result.markdown(f"""
    <div style="background:#fff0f5; padding:20px; border-radius:15px; font-size:20px; color:#c71585; box-shadow: 0 8px 20px rgba(199,21,133,0.3); max-width:600px; margin:auto;">
        {jobs_html}
    </div>
    """, unsafe_allow_html=True)

