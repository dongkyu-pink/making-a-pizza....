import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 페이지 기본 설정
st.set_page_config(page_title="화덕 피자 장인 게임", page_icon="🍕", layout="wide")

# CSS 및 레이아웃 스타일링 (피자집 분위기)
st.markdown("""
<style>
    .stApp {
        background-color: #2b1d17;
        background-image: radial-gradient(#3d2920 15%, transparent 16%), radial-gradient(#3d2920 15%, transparent 16%);
        background-size: 60px 60px;
        background-position: 0 0, 30px 30px;
        color: #ffffff;
    }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 데이터 정의 (피자 점수 각각 +2점 반영)
# ---------------------------------------------------------
ALL_INGREDIENTS = ["파", "버섯", "페퍼로니", "치즈", "케첩", "감자", "고구마", "꿀", "사과", "파인애플", "복숭아", "불고기"]

PIZZA_RECIPES = [
    {"name": "파피자", "score": 3, "ingredients": {"파", "케첩", "치즈"}},
    {"name": "버섯피자", "score": 3, "ingredients": {"버섯", "케첩", "치즈"}},
    {"name": "페퍼로니피자", "score": 3, "ingredients": {"페퍼로니", "케첩", "치즈"}},
    {"name": "치즈피자", "score": 3, "ingredients": {"케첩", "치즈"}},
    {"name": "피자", "score": 3, "ingredients": {"케첩"}},
    {"name": "감자피자", "score": 3, "ingredients": {"감자", "케첩", "치즈"}},
    {"name": "고구마피자", "score": 3, "ingredients": {"고구마", "케첩", "치즈"}},
    {"name": "사과피자", "score": 3, "ingredients": {"사과", "케첩", "치즈"}},
    {"name": "복숭아피자", "score": 3, "ingredients": {"복숭아", "케첩", "치즈"}},
    {"name": "불고기버섯피자", "score": 4, "ingredients": {"불고기", "버섯", "케첩", "치즈"}},
    {"name": "페퍼로니버섯피자", "score": 4, "ingredients": {"페퍼로니", "버섯", "케첩", "치즈"}},
    {"name": "감자페퍼로니피자", "score": 5, "ingredients": {"치즈", "케첩", "페퍼로니", "감자"}},
    {"name": "슈프림피자", "score": 5, "ingredients": {"케첩", "페퍼로니", "불고기", "버섯", "파"}},
    {"name": "고르곤졸라피자", "score": 5, "ingredients": {"꿀", "치즈", "복숭아", "고구마", "사과", "파인애플"}},
    {"name": "하와이안피자", "score": 5, "ingredients": {"치즈", "케첩", "파인애플", "페퍼로니"}},
    {"name": "콤비네이션피자", "score": 6, "ingredients": {"치즈", "케첩", "페퍼로니", "불고기", "버섯", "파"}},
]

HIDDEN_RECIPES = [
    {"name": "슈퍼 콤비네이션 피자", "score": 9, "ingredients": set(ALL_INGREDIENTS), "id": 1},
    {"name": "과일피자", "score": 7, "ingredients": {"사과", "복숭아", "파인애플"}, "id": 2}
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

def get_target_score():
    if st.session_state.difficulty == '쉬움':
        return 50
    elif st.session_state.difficulty == '어려움':
        return 100
    return "무제한"

def get_turn_limit():
    return 20 if st.session_state.difficulty == '쉬움' else 10

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
    st.caption("아늑한 분위기의 화덕 피자 전문점입니다.")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📋 메뉴판 공부하기")
        if st.button("주문표 열기"):
            st.session_state.page = 'menu'
            st.rerun()

    with col2:
        st.subheader("⚙️ 난이도 설정")
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
        st.write("2분(120초) 동안 최고의 피자를 구워내세요!")
        if st.button("🚀 영업 시작", type="primary"):
            start_game()
            st.rerun()

# ---------------------------------------------------------
# 페이지 2: 주문표 화면
# ---------------------------------------------------------
elif st.session_state.page == 'menu':
    st.title("📜 피자 레시피 주문표")
    if st.button("⬅️ 로비로 돌아가기"):
        st.session_state.page = 'lobby'
        st.rerun()
    st.divider()
    
    cols = st.columns(2)
    for idx, pizza in enumerate(PIZZA_RECIPES):
        with cols[idx % 2]:
            st.markdown(f"**{pizza['name']}** (+{pizza['score']}점)")
            st.write(f"- 필요 재료: {', '.join(pizza['ingredients'])}")
            st.write("---")

# ---------------------------------------------------------
# 페이지 3: 게임 플레이 화면 (요청해주신 구도 100% 반영)
# ---------------------------------------------------------
elif st.session_state.page == 'game':
    # 타이머 계산
    elapsed_game = time.time() - st.session_state.game_start_time
    remaining_game = max(0, 120 - int(elapsed_game))

    elapsed_turn = time.time() - st.session_state.turn_start_time
    remaining_turn = max(0, get_turn_limit() - int(elapsed_turn))

    if remaining_game <= 0:
        st.session_state.page = 'result'
        st.rerun()

    if remaining_turn <= 0:
        st.toast("⏳ 시간 초과! -1점 감점됩니다.", icon="❌")
        st.session_state.score -= 1
        next_turn()
        st.rerun()

    order = st.session_state.current_order
    target_score = get_target_score()

    # 상단 대시보드
    st.markdown(f"""
    <div style="border: 3px solid #e74c3c; border-radius: 12px; padding: 12px; background: #1e1e1e; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-around; align-items: center; font-size: 18px; font-weight: bold; color: #ffffff;">
            <div style="color: #ff7675;">🛎️ 주문: <span style="font-size: 22px; color: #ffeaa7;">{order['name']}</span></div>
            <div>⏱️ 판 남은시간: <span style="font-size: 22px; color: #00cec9;">{remaining_game}초</span></div>
            <div>⏳ 턴 남은시간: <span style="font-size: 22px; color: #ff7675;">{remaining_turn}초</span></div>
            <div>⭐ 현재점수: <span style="font-size: 22px; color: #fdcb6e;">{st.session_state.score}점</span></div>
            <div>🎯 목표점수: <span style="font-size: 22px; color: #55efc4;">{target_score}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1초 자동 타이머 갱신
    @st.fragment(run_every=1)
    def update_timer():
        cur_g = max(0, 120 - int(time.time() - st.session_state.game_start_time))
        cur_t = max(0, get_turn_limit() - int(time.time() - st.session_state.turn_start_time))
        if cur_g <= 0 or cur_t <= 0:
            st.rerun()
    update_timer()

    # 중앙 스케치 구도 (피자 도우 & 화덕 그래픽)
    main_col1, main_col2 = st.columns([1, 1])

    with main_col1:
        # 좌측: 원형 피자 도우 영역
        current_ings = ", ".join(st.session_state.selected_ingredients) if st.session_state.selected_ingredients else "재료 없음"
        baked_status = "♨️ 화덕 내부 구이 완료!" if st.session_state.baked else "⚪ 도우 위 재료 조합 중..."
        
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="
                width: 280px; height: 280px; border-radius: 50%;
                background-color: #fce4ec; border: 8px solid #f8bbd0;
                margin: 0 auto; display: flex; flex-direction: column;
                justify-content: center; align-items: center; color: #333;
                box-shadow: 0px 8px 15px rgba(0,0,0,0.3); position: relative;
            ">
                <h3 style="color: #d81b60; margin: 0;">🍕 피자 (흰색 도우)</h3>
                <p style="font-size: 14px; margin-top: 8px; font-weight: bold; color: #444;">
                    {baked_status}
                </p>
                <div style="background: rgba(255,255,255,0.8); padding: 5px 12px; border-radius: 12px; margin-top: 5px; max-width: 80%;">
                    <small style="color: #d81b60;"><b>[ 올린 재료 ]</b><br>{current_ings}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with main_col2:
        # 우측: 원형 화덕 영역
        st.markdown("""
        <div style="text-align: center;">
            <div style="
                width: 280px; height: 280px; border-radius: 50%;
                background: radial-gradient(circle, #ff7675 10%, #d63031 50%, #2d3436 90%);
                border: 8px solid #636e72; margin: 0 auto; display: flex;
                flex-direction: column; justify-content: center; align-items: center;
                box-shadow: 0px 8px 15px rgba(0,0,0,0.5); color: #ffeaa7;
            ">
                <h2 style="margin: 0; text-shadow: 2px 2px 4px #000;">🔥 화덕 그림</h2>
                <p style="font-size: 15px; color: #fff; margin-top: 10px;">뜨거운 불꽃 작동 중...</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 하단 구도 (우측 버튼 구역 & 전체 재료 드래그 앤 드롭 구역)
    col_bottom_left, col_bottom_right = st.columns([1.5, 1])

    with col_bottom_right:
        st.markdown("##### ⚙️ 기능 조작")
        if st.button("🔥 화덕에 굽기", use_container_width=True):
            st.session_state.baked = True
            st.toast("피자를 화덕에 구웠습니다!", icon="🔥")
            st.rerun()

        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("📤 제출하기", type="primary", use_container_width=True):
                if not st.session_state.baked:
                    st.warning("화덕에 먼저 구워주세요!")
                else:
                    current_set = st.session_state.selected_ingredients
                    hidden_triggered = False
                    for h in HIDDEN_RECIPES:
                        if current_set == h['ingredients']:
                            if not st.session_state.used_hidden[h['id']]:
                                st.session_state.score += h['score']
                                st.session_state.used_hidden[h['id']] = True
                                st.toast(f"✨ 히든 피자 완성! +{h['score']}점!", icon="🎉")
                            hidden_triggered = True
                            break
                    
                    if not hidden_triggered:
                        if current_set == order['ingredients']:
                            st.session_state.score += order['score']
                            st.toast(f"✅ 완성! +{order['score']}점!", icon="👏")
                        else:
                            st.session_state.score -= 1
                            st.toast("❌ 잘못된 피자입니다! -1점 감점", icon="💥")
                    next_turn()
                    st.rerun()

        with b_c2:
            if st.button("🗑️ 버리기", use_container_width=True):
                st.toast("피자를 버렸습니다.")
                next_turn()
                st.rerun()

    with col_bottom_left:
        st.markdown("##### 🛒 재료 목록 (클릭하여 도우에 올리기)")
        # 셀렉터 형태로 재료를 끌어서 도우 위 추가 가능하도록 구현
        selected = st.multiselect(
            "마우스로 재료를 선택하여 도우로 넣으세요:", 
            ALL_INGREDIENTS, 
            default=list(st.session_state.selected_ingredients)
        )
        st.session_state.selected_ingredients = set(selected)

# ---------------------------------------------------------
# 페이지 4: 결과 화면
# ---------------------------------------------------------
elif st.session_state.page == 'result':
    st.title("🏁 영업 종료 - 최종 성과")
    st.divider()

    score = st.session_state.score
    diff = st.session_state.difficulty

    if score > st.session_state.high_score:
        st.session_state.high_score = score

    if diff == '쉬움':
        st.subheader(f"최종 획득 점수: **{score}점** (목표 50점)")
        if score >= 50:
            st.balloons()
            st.success("🎉 목표 달성 성공! 부자가 되셨습니다! 💵💶💷")
        else:
            st.error("😭 파산했습니다... 피자가게 문을 닫습니다. 💸")

    elif diff == '어려움':
        st.subheader(f"최종 획득 점수: **{score}점** (목표 100점)")
        if score >= 100:
            st.balloons()
            st.success("🎉 목표 달성 성공! 100점 돌파! 💵💶💷")
        else:
            st.error("😭 목표 점수에 도달하지 못했습니다.")

    elif diff == '한계':
        st.balloons()
        st.markdown(f"## 🎉 당신의 최고 기록: **'{score}'점**")

    st.divider()
    if st.button("🔄 다시 시작 (로비로 돌아가기)", type="primary"):
        st.session_state.page = 'lobby'
        st.rerun()
