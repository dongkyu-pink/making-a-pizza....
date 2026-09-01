import streamlit as st
import random
import time

# 페이지 기본 설정
st.set_page_config(page_title="화덕 피자 장인 게임", page_icon="🍕", layout="wide")

# CSS 스타일링 (가게 분위기 연출 및 카드 디자인)
st.markdown("""
<style>
    .main {
        background-color: #fbf8f3;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .pizza-box {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .oven-box {
        background-color: #3a2e2b;
        color: #ff9d42;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 데이터 정의
# ---------------------------------------------------------
ALL_INGREDIENTS = ["파", "버섯", "페퍼로니", "치즈", "케첩", "감자", "고구마", "꿀", "사과", "파인애플", "복숭아", "불고기"]

PIZZA_RECIPES = [
    {"name": "파피자", "score": 1, "ingredients": {"파", "케첩", "치즈"}},
    {"name": "버섯피자", "score": 1, "ingredients": {"버섯", "케첩", "치즈"}},
    {"name": "페퍼로니피자", "score": 1, "ingredients": {"페퍼로니", "케첩", "치즈"}},
    {"name": "치즈피자", "score": 1, "ingredients": {"케첩", "치즈"}},
    {"name": "피자", "score": 1, "ingredients": {"케첩"}},
    {"name": "감자피자", "score": 1, "ingredients": {"감자", "케첩", "치즈"}},
    {"name": "고구마피자", "score": 1, "ingredients": {"고구마", "케첩", "치즈"}},
    {"name": "사과피자", "score": 1, "ingredients": {"사과", "케첩", "치즈"}},
    {"name": "복숭아피자", "score": 1, "ingredients": {"복숭아", "케첩", "치즈"}},
    {"name": "불고기버섯피자", "score": 2, "ingredients": {"불고기", "버섯", "케첩", "치즈"}},
    {"name": "페퍼로니버섯피자", "score": 2, "ingredients": {"페퍼로니", "버섯", "케첩", "치즈"}},
    {"name": "감자페퍼로니피자", "score": 3, "ingredients": {"치즈", "케첩", "페퍼로니", "감자"}},
    {"name": "슈프림피자", "score": 3, "ingredients": {"케첩", "페퍼로니", "불고기", "버섯", "파"}},
    {"name": "고르곤졸라피자", "score": 3, "ingredients": {"꿀", "치즈", "복숭아", "고구마", "사과", "파인애플"}},
    {"name": "하와이안피자", "score": 3, "ingredients": {"치즈", "케첩", "파인애플", "페퍼로니"}},
    {"name": "콤비네이션피자", "score": 4, "ingredients": {"치즈", "케첩", "페퍼로니", "불고기", "버섯", "파"}},
]

HIDDEN_RECIPES = [
    {"name": "슈퍼 콤비네이션 피자", "score": 7, "ingredients": set(ALL_INGREDIENTS), "id": 1},
    {"name": "과일피자", "score": 5, "ingredients": {"사과", "복숭아", "파인애플"}, "id": 2}
]

# ---------------------------------------------------------
# 세션 상태 초기화
# ---------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'lobby'
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = '쉬움'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_start_time' not in st.session_state:
    st.session_state.game_start_time = 0
if 'turn_start_time' not in st.session_state:
    st.session_state.turn_start_time = 0
if 'current_order' not in st.session_state:
    st.session_state.current_order = None
if 'selected_ingredients' not in st.session_state:
    st.session_state.selected_ingredients = set()
if 'baked' not in st.session_state:
    st.session_state.baked = False
if 'used_hidden' not in st.session_state:
    st.session_state.used_hidden = {1: False, 2: False}
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

def get_turn_limit():
    if st.session_state.difficulty == '쉬움':
        return 20
    elif st.session_state.difficulty == '어려움':
        return 10
    else:  # 한계 난이도 (10초로 설정)
        return 10

def next_turn():
    st.session_state.current_order = random.choice(PIZZA_RECIPES)
    st.session_state.selected_ingredients = set()
    st.session_state.baked = False
    st.session_state.turn_start_time = time.time()

def start_game():
    st.session_state.score = 0
    st.session_state.used_hidden = {1: False, 2: False}
    st.session_state.game_start_time = time.time()
    st.session_state.page = 'game'
    next_turn()

# ---------------------------------------------------------
# 페이지 1: 로비 화면
# ---------------------------------------------------------
if st.session_state.page == 'lobby':
    st.title("🍕 화덕 피자 가게에 오신 것을 환영합니다!")
    st.caption("따뜻한 화덕이 기다리고 있는 최고의 피자집입니다.")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📋 메뉴판 공부하기")
        if st.button("주문표 열기"):
            st.session_state.page = 'menu'
            st.rerun()

    with col2:
        st.subheader("⚙️ 난이도 설정")
        # 라디오 버튼 선택값에 따라 즉시 난이도가 정확하게 매칭되도록 수정
        selected_diff = st.radio(
            "난이도 선택", 
            ["쉬움", "어려움", "한계"], 
            index=["쉬움", "어려움", "한계"].index(st.session_state.difficulty)
        )
        st.session_state.difficulty = selected_diff
        
        if selected_diff == "쉬움":
            st.info("선택된 난이도: **쉬움** (턴당 20초 / 목표 50점)")
        elif selected_diff == "어려움":
            st.warning("선택된 난이도: **어려움** (턴당 10초 / 목표 100점)")
        else:
            st.error("선택된 난이도: **한계** (턴당 10초 / 점수 한계 도전)")

    with col3:
        st.subheader("🔥 가게 열기")
        st.write("2분간 제한시간 동안 피자를 만들어 제공하세요!")
        if st.button("🚀 영업 시작", type="primary"):
            start_game()
            st.rerun()

# ---------------------------------------------------------
# 페이지 2: 주문표 화면
# ---------------------------------------------------------
elif st.session_state.page == 'menu':
    st.title("📜 피자 주문표 (레시피)")
    st.write("각 피자의 점수와 필요한 재료를 미리 숙지하세요!")
    
    if st.button("⬅️ 로비로 돌아가기"):
        st.session_state.page = 'lobby'
        st.rerun()

    st.divider()
    
    st.subheader("🍕 일반 피자 메뉴")
    cols = st.columns(2)
    for idx, pizza in enumerate(PIZZA_RECIPES):
        with cols[idx % 2]:
            st.markdown(f"**{pizza['name']}** ({pizza['score']}점)")
            st.write(f"- 재료: {', '.join(pizza['ingredients'])}")
            st.write("---")

    st.subheader("❓ 히든 피자 메뉴")
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        st.markdown("<div style='background-color: #222; color: #fff; padding: 15px; border-radius: 8px;'>🔒 ??? (검은 피자 판 1)<br>점수: 7점<br>재료: ❓❓❓</div>", unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div style='background-color: #222; color: #fff; padding: 15px; border-radius: 8px;'>🔒 ??? (검은 피자 판 2)<br>점수: 5점<br>재료: ❓❓❓</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 페이지 3: 게임 플레이 화면
# ---------------------------------------------------------
elif st.session_state.page == 'game':
    elapsed_game_time = time.time() - st.session_state.game_start_time
    remaining_game_time = max(0, 120 - int(elapsed_game_time))

    elapsed_turn_time = time.time() - st.session_state.turn_start_time
    turn_limit = get_turn_limit()
    remaining_turn_time = max(0, turn_limit - int(elapsed_turn_time))

    # 게임 전체 시간 종료 체크
    if remaining_game_time <= 0:
        st.session_state.page = 'result'
        st.rerun()

    # 턴 시간 초과 체크
    if remaining_turn_time <= 0:
        st.toast("⏳ 시간 초과! 1점이 감점됩니다.", icon="❌")
        st.session_state.score -= 1
        next_turn()
        st.rerun()

    col_score, col_gtime, col_ttime = st.columns(3)
    col_score.metric("현재 점수", f"{st.session_state.score} 점")
    col_gtime.metric("남은 전체 시간", f"{remaining_game_time} 초")
    col_ttime.metric("현재 턴 남은 시간", f"{remaining_turn_time} 초")

    st.divider()

    order = st.session_state.current_order
    st.markdown(f"<h2 style='text-align: center; color: #d9534f;'>🛎️ 주문: {order['name']}</h2>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("🛒 재료 선택")
        st.caption("클릭하여 피자 위에 재료를 올리거나 뺍니다.")
        
        ing_cols = st.columns(3)
        for idx, ing in enumerate(ALL_INGREDIENTS):
            with ing_cols[idx % 3]:
                is_selected = ing in st.session_state.selected_ingredients
                btn_label = f"✅ {ing}" if is_selected else f"+ {ing}"
                if st.button(btn_label, key=f"ing_{ing}"):
                    if is_selected:
                        st.session_state.selected_ingredients.remove(ing)
                    else:
                        st.session_state.selected_ingredients.add(ing)
                    st.rerun()

    with col_right:
        st.subheader("🔥 화덕 및 피자 판")
        
        current_set = st.session_state.selected_ingredients
        pizza_name = "도우 (빈 피자)"
        
        matched_pizza = None
        for h in HIDDEN_RECIPES:
            if current_set == h['ingredients']:
                matched_pizza = h
                break
        if not matched_pizza:
            for p in PIZZA_RECIPES:
                if current_set == p['ingredients']:
                    matched_pizza = p
                    break
        
        if matched_pizza:
            pizza_name = matched_pizza['name']
        elif len(current_set) > 0:
            pizza_name = "괴상한 피자"

        if st.session_state.baked:
            st.markdown(f"""
            <div class='oven-box'>
                🔴 화덕 내부 작동 중... ♨️<br><br>
                <h3>[ 완성된 피자: {pizza_name} ]</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='pizza-box'>
                ⚪ 피자 도우 위 올려진 재료:<br>
                <b>{', '.join(st.session_state.selected_ingredients) if st.session_state.selected_ingredients else '없음'}</b><br><br>
                <h4>현재 피자: {pizza_name}</h4>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        if st.button("🔥 화덕에 굽기"):
            st.session_state.baked = True
            st.rerun()

        st.write("---")
        
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("📤 제출하기", type="primary"):
                if not st.session_state.baked:
                    st.warning("화덕에 피자를 먼저 구워주세요!")
                else:
                    hidden_triggered = False
                    for h in HIDDEN_RECIPES:
                        if current_set == h['ingredients']:
                            if not st.session_state.used_hidden[h['id']]:
                                st.session_state.score += h['score']
                                st.session_state.used_hidden[h['id']] = True
                                st.toast(f"✨ 히든 피자 완성! [{h['name']}] +{h['score']}점!", icon="🎉")
                            else:
                                st.toast("이미 이번 판에서 제출한 히든 피자입니다! 0점 처리됩니다.", icon="⚠️")
                            hidden_triggered = True
                            break
                    
                    if not hidden_triggered:
                        if current_set == order['ingredients']:
                            st.session_state.score += order['score']
                            st.toast(f"✅ 정답! +{order['score']}점 획득!", icon="👏")
                        else:
                            st.session_state.score -= 1
                            st.toast("❌ 잘못된 피자입니다! -1점 감점!", icon="💥")
                    
                    next_turn()
                    st.rerun()

        with btn_col2:
            if st.button("🗑️ 버리기"):
                st.toast("피자를 버렸습니다. 새로운 턴을 시작합니다.")
                next_turn()
                st.rerun()

# ---------------------------------------------------------
# 페이지 4: 결과 화면
# ---------------------------------------------------------
elif st.session_state.page == 'result':
    st.title("🏁 영업 종료 - 결과 발표")
    st.divider()

    score = st.session_state.score
    diff = st.session_state.difficulty

    if score > st.session_state.high_score:
        st.session_state.high_score = score

    # 1. 쉬움 난이도 결과
    if diff == '쉬움':
        st.subheader(f"최종 획득 점수: **{score}점** (목표: 50점)")
        if score >= 50:
            st.balloons()
            st.success("🎉 축하합니다! 목표를 달성했습니다! 부자가 되어 돈이 펑펑 휘날립니다! 💵💶💷")
            st.markdown("# 🤑 💰 💸 💰 💸")
        else:
            st.error("😭 파산했습니다... 피자가게 문을 닫습니다. 💸")
            st.markdown("# 💸 🧎‍♂️ (털썩...)")

    # 2. 어려움 난이도 결과
    elif diff == '어려움':
        st.subheader(f"최종 획득 점수: **{score}점** (목표: 100점)")
        if score >= 100:
            st.balloons()
            st.success("🎉 축하합니다! 100점 이상 달성! 부자가 되어 돈이 펑펑 휘날립니다! 💵💶💷")
            st.markdown("# 🤑 💰 💸 💰 💸")
        else:
            st.error("😭 파산했습니다... 목표 점수에 도달하지 못했습니다.")
            st.markdown("# 💸 🧎‍♂️ (털썩...)")

    # 3. 한계 난이도 결과 (파산/부자 없이 정확한 축하 문구 출력)
    elif diff == '한계':
        st.balloons()
        st.markdown(f"## 🎉 축하합니다! 당신은 **'{score}'** 의 점수를 획득했습니다!")
        st.info(f"🏆 최고 점수 기록: **{st.session_state.high_score}점**")

    st.divider()
    if st.button("🔄 다시 시작 (로비로 돌아가기)", type="primary"):
        st.session_state.page = 'lobby'
        st.rerun()
