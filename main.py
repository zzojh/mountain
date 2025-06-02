import streamlit as st

import streamlit as st

st.set_page_config(page_title="🌟 MBTI 진로 추천기 🌟", layout="centered")

# --- CSS & JS 커튼 애니메이션 ---
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 타이틀 */
.title {
    text-align: center;
    font-size: 48px;
    color: #FF69B4;
    font-weight: 900;
    margin-bottom: 10px;
    user-select: none;
}

.subtitle {
    text-align: center;
    font-size: 24px;
    color: #9370DB;
    margin-bottom: 40px;
    user-select: none;
}

/* 커튼 컨테이너 */
.curtain-container {
    position: relative;
    width: 100%;
    height: 200px;
    margin: 0 auto;
    overflow: hidden;
    margin-bottom: 40px;
}

/* 왼쪽 커튼 */
.curtain-left {
    position: absolute;
    width: 50%;
    height: 100%;
    top: 0;
    left: 0;
    background: linear-gradient(135deg, #ff6a88 0%, #ff99ac 100%);
    box-shadow: 5px 0 20px rgba(0,0,0,0.3);
    transform-origin: left;
    animation-fill-mode: forwards;
    animation-duration: 1.5s;
}

/* 오른쪽 커튼 */
.curtain-right {
    position: absolute;
    width: 50%;
    height: 100%;
    top: 0;
    right: 0;
    background: linear-gradient(135deg, #ff6a88 0%, #ff99ac 100%);
    box-shadow: -5px 0 20px rgba(0,0,0,0.3);
    transform-origin: right;
    animation-fill-mode: forwards;
    animation-duration: 1.5s;
}

/* 커튼 열리는 애니메이션 */
@keyframes openLeft {
    from { transform: translateX(0) rotateY(0deg); }
    to { transform: translateX(-100%) rotateY(-90deg); }
}

@keyframes openRight {
    from { transform: translateX(0) rotateY(0deg); }
    to { transform: translateX(100%) rotateY(90deg); }
}

/* 추천 직업 박스 */
.job-box {
    background-color: #FFF0F5;
    padding: 20px 40px;
    border-radius: 15px;
    font-size: 22px;
    font-weight: 600;
    color: #C71585;
    box-shadow: 0 8px 20px rgba(199,21,133,0.3);
    max-width: 600px;
    margin: 0 auto;
    opacity: 0;
    animation-fill-mode: forwards;
    animation-duration: 1s;
    animation-delay: 1.5s;
}

/* 나타나는 애니메이션 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.job-box.show {
    animation-name: fadeInUp;
}

</style>
""", unsafe_allow_html=True)

# --- 타이틀 ---
st.markdown('<div class="title">🌟 MBTI 진로 추천기 🌟</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">당신의 성격에 딱 맞는 직업을 찾아보세요! 😎💼</div>', unsafe_allow_html=True)

# --- MBTI 선택 ---
mbti_options = [
    "INTJ 🧠", "INTP 🤯", "ENTJ 👑", "ENTP 🧪",
    "INFJ 🌌", "INFP 🌸", "ENFJ 🎤", "ENFP 🌈",
    "ISTJ 🗂️", "ISFJ 🫶", "ESTJ 🧱", "ESFJ 🤝",
    "ISTP 🔧", "ISFP 🎨", "ESTP 🏎️", "ESFP 🎉"
]

mbti_choice = st.selectbox("👇 당신의 MBTI를 선택하세요!", mbti_options)

# --- 직업 데이터 ---
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

# --- 커튼 & 결과 출력 ---
if mbti_choice:
    # 커튼 애니메이션 div
    st.markdown("""
    <div class="curtain-container">
        <div class="curtain-left" style="animation-name: openLeft;"></div>
        <div class="curtain-right" style="animation-name: openRight;"></div>
    </div>
    """, unsafe_allow_html=True)

    # 추천 직업 박스 (애니메이션 지연시간 맞춰서 나타남)
    jobs = mbti_jobs.get(mbti_choice, [])
    jobs_html = "<ul>"
    for job in jobs:
        jobs_html += f"<li>🎯 {job}</li>"
    jobs_html += "</ul>"

    st.markdown(f"""
    <div class="job-box show">
    {jobs_html}
    </div>
    """, unsafe_allow_html=True)
