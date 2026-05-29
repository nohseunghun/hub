import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="연애 코칭 앱",
    page_icon="💌",
    layout="centered"
)

# 스타일
st.markdown(
    """
    <style>
    .main {
        background-color: #fff5f7;
    }
    .title {
        text-align: center;
        color: #ff4b6e;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .tip-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ff4b6e;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 제목
st.markdown('<div class="title">💌 AI 연애 코칭 앱</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">상황에 맞는 연애 조언과 대화 추천을 받아보세요!</div>',
    unsafe_allow_html=True
)

# 사이드바
st.sidebar.header("⚙️ 사용자 정보")
name = st.sidebar.text_input("이름", "사용자")
age = st.sidebar.slider("나이", 18, 50, 25)
relationship = st.sidebar.selectbox(
    "현재 상태",
    ["썸", "연애 중", "짝사랑", "이별 후", "소개팅 준비"]
)

# 메인 기능
st.header("📍 현재 상황 입력")
user_input = st.text_area(
    "연애 고민이나 상황을 자세히 적어주세요",
    placeholder="예: 좋아하는 사람이 있는데 먼저 연락해도 될지 고민이에요...",
    height=180
)

# 감정 선택
emotion = st.selectbox(
    "현재 감정",
    ["설렘", "불안", "긴장", "행복", "우울", "혼란스러움"]
)

# 연애 조언 함수
def generate_coaching(text, relation, feeling):
    text = text.lower()

    if "연락" in text:
        return "상대에게 부담되지 않게 가볍고 자연스럽게 연락해보세요. 짧은 안부나 공통 관심사로 시작하는 것이 좋아요. 😊"

    elif "고백" in text:
        return "고백은 타이밍이 중요합니다. 상대와 충분한 교감이 쌓였다면 솔직한 마음을 전해보세요."

    elif "이별" in text or relation == "이별 후":
        return "지금은 감정을 억누르기보다 충분히 정리하는 시간이 필요합니다. 스스로를 돌보는 것이 가장 중요해요. 💙"

    elif relation == "썸":
        return "썸 단계에서는 상대를 알아가는 과정이 중요합니다. 너무 조급해하지 말고 편안한 분위기를 만들어보세요."

    elif relation == "소개팅 준비":
        return "소개팅에서는 자연스러운 미소와 경청이 가장 큰 매력입니다. 상대의 이야기에 공감해보세요."

    else:
        return "연애에서는 솔직한 대화와 상대에 대한 배려가 가장 중요합니다. 자신의 감정도 소중히 생각하세요. ✨"

# 추천 멘트 함수
def recommend_message(relation):
    messages = {
        "썸": "오늘 뭐 했어? 갑자기 네 생각나서 연락해봤어 😊",
        "연애 중": "오늘도 고생했어 ❤️ 맛있는 거 먹고 푹 쉬어!",
        "짝사랑": "너랑 이야기하면 시간 가는 줄 모르겠어 😄",
        "이별 후": "지금은 나 자신을 더 아껴주고 성장하는 시간이야.",
        "소개팅 준비": "오늘 만나서 즐거웠어요! 다음에 또 이야기하고 싶네요 😊"
    }
    return messages.get(relation, "좋은 하루 보내 😊")

# 버튼
if st.button("💡 연애 코칭 받기"):
    if user_input.strip() == "":
        st.warning("연애 고민을 입력해주세요!")
    else:
        advice = generate_coaching(user_input, relationship, emotion)
        message = recommend_message(relationship)

        st.success(f"{name}님을 위한 연애 코칭 결과입니다!")

        st.markdown("### ❤️ AI 연애 조언")
        st.markdown(f'<div class="tip-box">{advice}</div>', unsafe_allow_html=True)

        st.markdown("### 💬 추천 대화 멘트")
        st.info(message)

        st.markdown("### 📊 현재 감정 분석")
        st.write(f"현재 감정 상태: **{emotion}**")

        if emotion == "불안":
            st.write("→ 상대 반응에 너무 의미를 부여하지 말고 여유를 가져보세요.")
        elif emotion == "설렘":
            st.write("→ 좋은 에너지가 느껴집니다! 자연스럽게 표현해보세요.")
        elif emotion == "우울":
            st.write("→ 자신의 감정을 충분히 돌보는 시간이 필요합니다.")
        else:
            st.write("→ 감정을 솔직하게 표현하는 것이 관계에 도움이 됩니다.")

# 오늘의 연애 팁
st.markdown("---")
st.subheader("🌸 오늘의 연애 팁")

love_tips = [
    "좋은 관계는 작은 배려에서 시작됩니다.",
    "상대의 말을 끝까지 들어주는 것만으로도 큰 호감이 됩니다.",
    "억지로 맞추기보다 자연스러운 모습이 더 매력적입니다.",
    "연애에서도 자기 자신을 잃지 않는 것이 중요합니다.",
    "진심 어린 칭찬은 관계를 더 가깝게 만듭니다."
]

current_tip = love_tips[datetime.now().day % len(love_tips)]
st.info(current_tip)

# 푸터
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
