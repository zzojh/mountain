import streamlit as st



# 🎨 스타일링을 위한 HTML 사용
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 48px;
        color: #FF69B4;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        font-size: 24px;
        color: #9370DB;
    }
    .job-box {
        background-color: #FFF0F5;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 🎉 타이틀
st.markdown('<div class="title">🌟 MBTI 진로 추천기 🌟</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">당신의 성격에 딱 맞는 직업을 찾아보세요! 😎💼</div>', unsafe_allow_html=True)

# 🧠 MBTI 선택
mbti_options = [
    "INTJ 🧠", "INTP 🤯", "ENTJ 👑", "ENTP 🧪",
    "INFJ 🌌", "INFP 🌸", "ENFJ 🎤", "ENFP 🌈",
    "ISTJ 🗂️", "ISFJ 🫶", "ESTJ 🧱", "ESFJ 🤝",
    "ISTP 🔧", "ISFP 🎨", "ESTP 🏎️", "ESFP 🎉"
]

mbti_choice = st.selectbox("👇 당신의 MBTI를 선택하세요!", mbti_options)

# 💼 MBTI별 추천 직업
mbti_jobs = {
    "INTJ 🧠": ["데이터 사이언티스트 📊", "전략 컨설턴트 🧩", "AI 연구원 🤖"],
    "INTP 🤯": ["이론 물리학자 ⚛️", "프로덕트 디자이너 🛠️", "프로그래머 👨‍💻"],
    "ENTJ 👑": ["CEO 🧑‍💼", "프로젝트 매니저 📈", "벤처 캐피탈리스트 💰"],
    "ENTP 🧪": ["스타트업 창업가 🚀", "마케팅 전략가 📣", "UX 디자이너 🧠"],
    "INFJ 🌌": ["상담사 🗣️", "인권 변호사 ⚖️", "작가 ✍️"],
    "INFP 🌸": ["예술가 🎨", "시인 📜", "사회운동가 ✊"],
    "ENFJ 🎤": ["교사 🍎", "연설가 🎙️", "리더십 코치 💼"],
    "ENFP 🌈": ["모험가 🌍", "방송인 📺", "콘텐츠 크리에이터 🎬"],
    "ISTJ 🗂️": ["회계사 💼", "법률 사무원 📑", "관리자 🧾"],
    "ISFJ 🫶": ["간호사 🏥", "교사 📘", "복지사 🫂"],
    "ESTJ 🧱": ["경영 관리자 🏢", "군 간부 🪖", "프로젝트 매니저 📋"],
    "ESFJ 🤝": ["이벤트 플래너 🎈", "상담교사 🧑‍🏫", "사회복지사 💖"],
    "ISTP 🔧": ["엔지니어 🔩", "기술자 🛠️", "자동차 정비사 🚗"],
    "ISFP 🎨": ["플로리스트 🌷", "패션 디자이너 👗", "사진작가 📸"],
    "ESTP 🏎️": ["세일즈 매니저 🏁", "스턴트 배우 🎭", "응급 구조사 🚑"],
    "ESFP 🎉": ["배우 🎬", "공연 기획자 🎼", "유튜버 📹"]
}

# 🧾 결과 출력
if mbti_choice:
    st.markdown("## 🎯 추천 직업 리스트")
    mbti_clean = mbti_choice.split(" ")[0]
    jobs = mbti_jobs.get(mbti_choice, [])
    
    st.markdown('<div class="job-box">', unsafe_allow_html=True)
    for job in jobs:
        st.markdown(f"- {job}")
    st.markdown('</div>', unsafe_allow_html=True)

# 🎁 푸터
st.markdown("---")
st.markdown("Made with ❤️ by [Your Name or Team]", unsafe_allow_html=True)
