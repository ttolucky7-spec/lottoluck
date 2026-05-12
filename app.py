import streamlit as st
import streamlit.components.v1 as components
import lotto
import time

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="로또 번호 생성기", page_icon="🎯", layout="centered")

st.markdown("""
<style>

div.stButton > button {
    width:100%;
    height:60px;

    background:linear-gradient(135deg, #2fb344, #51cf66);

    color:white;

    font-size:22px;
    font-weight:bold;

    border:none;
    border-radius:16px;

    box-shadow:0 4px 12px rgba(0,0,0,0.15);

    transition:all 0.2s ease;
}

div.stButton > button:hover {
    transform:translateY(-2px);
    box-shadow:0 6px 18px rgba(0,0,0,0.2);
}

</style>
""", unsafe_allow_html=True)

header_html = """
<div style='
    background-color:#ffffff;
    padding:28px;
    border-radius:20px;
    box-shadow:0 2px 10px rgba(0,0,0,0.06);
    margin-bottom:20px;
    text-align:center;
'>

<h1 style='
    margin:0;
    font-size:clamp(28px, 5vw, 42px);
    white-space:nowrap;
'>
🍀 행운 로또 번호 생성기
</h1>

<p style='
    color:#666;
    margin-top:10px;
    font-size:16px;
'>
번호 생성 방식을 선택하고 행운 번호를 받아보세요.
</p>

</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

MAX_ROUND = 1222

# -----------------------------
# 생성 방식 선택
# -----------------------------

with st.container():

    st.subheader("번호 설정")

    mode = st.radio("행운 번호 생성 방식", ["당첨 데이터 기반 생성", "자동 생성"])

    # -----------------------------
    # 회차 설정
    # -----------------------------
    if mode == "당첨 데이터 기반 생성":

        start = st.number_input("시작 회차", min_value=1, max_value=MAX_ROUND, value=1)

        end = st.number_input(
            "종료 회차", min_value=1, max_value=MAX_ROUND, value=MAX_ROUND
        )

    # -----------------------------
    # 고급 필터
    # -----------------------------
    with st.expander("고급 필터"):

        use_filter = st.checkbox("필터 사용")

        # 기본값
        odd_count = None
        even_count = None
        max_consecutive = None

        user_numbers = []

        odd_count = st.selectbox(
            "홀수 개수 선택", ["사용 안함", 0, 1, 2, 3, 4, 5, 6], index=0
        )

        if odd_count == "사용 안함":

            odd_count = None
            even_count = None

        else:

            even_count = 6 - odd_count

        max_consecutive = st.selectbox(
            "최대 연속 숫자 허용", ["사용 안함", 1, 2, 3, 4, 5, 6], index=0
        )

        if max_consecutive == "사용 안함":

            max_consecutive = None

        user_numbers = st.multiselect(
            "고정 번호 선택 (반자동)", range(1, 46), max_selections=6
        )




# -----------------------------
# 번호 생성 버튼
# -----------------------------
if st.button("행운 번호 받기"):

    with st.spinner("당신의 행운을 부르는 중..🍀"):

        time.sleep(1)

    # 회차 검사
    if mode == "당첨 데이터 기반 생성" and start > end:

        st.error("시작 회차가 종료 회차보다 클 수 없습니다.")

    # 고정 번호 검사
    elif len(user_numbers) > 6:

        st.error("고정 번호는 최대 6개까지 선택 가능합니다.")

    else:

        results = set()

        attempts = 0

        # -----------------------------
        # 당첨 데이터 기반 생성
        # -----------------------------
        if mode == "당첨 데이터 기반 생성":

            numbers = lotto.load_excel_data(start, end)

            while len(results) < 5 and attempts < 100:

                result = tuple(
                    lotto.generate_numbers(
                        numbers, user_numbers, odd_count, even_count, max_consecutive
                    )
                )

                results.add(result)

                attempts += 1

        # -----------------------------
        # 완전 랜덤 생성
        # -----------------------------
        else:

            while len(results) < 5 and attempts < 100:

                result = tuple(
                    lotto.generate_random_numbers(
                        user_numbers, odd_count, even_count, max_consecutive
                    )
                )

                results.add(result)

                attempts += 1

        # -----------------------------
        # 번호 색상 함수
        # -----------------------------
        def get_ball_color(num):

            if num <= 10:
                return "#fbc400"

            elif num <= 20:
                return "#69c8f2"

            elif num <= 30:
                return "#ff7272"

            elif num <= 40:
                return "#aaaaaa"

            else:
                return "#b0d840"

        # -----------------------------
        # 결과 출력
        # -----------------------------

        result_header = """
        <div style='
            background-color:#ffffff;
            padding:20px;
            border-radius:18px;
            box-shadow:0 2px 10px rgba(0,0,0,0.06);
            margin-top:30px;
            margin-bottom:20px;
        '>

        <h2 style='
            margin:0;
            font-size:26px;
        '>
        🍀 당신을 위한 행운 세트
        </h2>

        </div>
        """

        st.markdown(result_header, unsafe_allow_html=True)        

        copy_text = ""

        for i, combo in enumerate(results):

            # 세트 제목
            st.markdown(
            f"""
            <div style='
                font-size:20px;
                font-weight:600;
                margin-top:20px;
                margin-bottom:8px;
            '>
                {i+1}세트
            </div>
            """,
            unsafe_allow_html=True
        )

            # 번호 영역 시작
            number_html = """
            <div style="
                display:flex;
                gap:10px;
                flex-wrap:nowrap;
                margin-bottom:8px;
            ">
            """

            # 번호 반복
            for num in combo:

                # 번호 색상
                if 1 <= num <= 10:
                    color = "#fbc400"

                elif 11 <= num <= 20:
                    color = "#69c8f2"

                elif 21 <= num <= 30:
                    color = "#ff7272"

                elif 31 <= num <= 40:
                    color = "#aaaaaa"

                else:
                    color = "#b0d840"

                # 공 추가
                number_html += f"""
        <div style="
            width:45px;
            height:45px;
            border-radius:50%;
            background-color:{color};
            color:white;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:bold;
            font-size:18px;
            flex-shrink:0;
        ">
            {num}
        </div>
        """

            # 번호 영역 종료
            number_html += "</div>"

            # 출력
            st.markdown(number_html, unsafe_allow_html=True)

            # 복사용 텍스트
            line = f"{i+1}세트 : {', '.join(map(str, combo))}"

            copy_text += line + "\n"

        # -----------------------------
        # 전체 번호 복사 버튼
        # -----------------------------
        copy_button_html = f"""
        <div style="margin-top:30px;">

        <button onclick="
        navigator.clipboard.writeText(`{copy_text}`);
        alert('✅ 번호 복사 완료!');
        "

        style="
            width:100%;
            max-width:100%;
            box-sizing:border-box;

            background:linear-gradient(135deg, #2fb344, #51cf66);

            color:white;

            border:none;
            border-radius:16px;

            padding:16px;

            font-size:20px;
            font-weight:bold;

            cursor:pointer;

            box-shadow:0 4px 12px rgba(0,0,0,0.15);

            transition:all 0.2s ease;
        "
        onmouseover="
            this.style.transform='translateY(-2px)';
            this.style.boxShadow='0 6px 18px rgba(0,0,0,0.2)';
        "
        onmouseout="
            this.style.transform='translateY(0px)';
            this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)';
        ">
        ✨ 행운번호 복사
        </button>

        </div>
        """

        components.html(copy_button_html, height=100)

        # -----------------------------
        # 부족 경고
        # -----------------------------
        if len(results) < 5:

            st.warning("일부 조합이 중복되어 5세트를 모두 생성하지 못했습니다.")
