import streamlit as st
import streamlit.components.v1 as components
import random
import time
from streamlit_autorefresh import st_autorefresh

# 페이지 기본 설정
st.set_page_config(page_title="화덕 피자 장인 게임", page_icon="🍕", layout="wide")

# CSS 스타일링
st.markdown("""
<style>
    .main { background-color: #fbf8f3; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .pizza-box {
        background-color: #ffffff;
        border: 2px dashed #b5b5b5;
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

def get_turn_limit():
    if st.session_state.difficulty == '쉬움':
        return 20
    else:  # 어려움, 한계
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
    st.write("각 피자의 점수(+2점 적용됨)와 필요한 재료를 미리 숙지하세요!")
    
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
        st.markdown("<div style='background-color: #222; color: #fff; padding: 15px; border-radius: 8px;'>🔒 ??? (검은 피자 판 1)<br>점수: 9점<br>재료: ❓❓❓</div>", unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div style='background-color: #222; color: #fff; padding: 15px; border-radius: 8px;'>🔒 ??? (검은 피자 판 2)<br>점수: 7점<br>재료: ❓❓❓</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 페이지 3: 게임 플레이 화면
# ---------------------------------------------------------
elif st.session_state.page == 'game':
    # 1초마다 실시간 화면 자동 타이머 갱신
    st_autorefresh(interval=1000, key="gametimer")

    elapsed_game_time = time.time() - st.session_state.game_start_time
    remaining_game_time = max(0, 120 - int(elapsed_game_time))

    elapsed_turn_time = time.time() - st.session_state.turn_start_time
    turn_limit = get_turn_limit()
    remaining_turn_time = max(0, turn_limit - int(elapsed_turn_time))

    if remaining_game_time <= 0:
        st.session_state.page = 'result'
        st.rerun()

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
        st.subheader("🖐️ 재료 드래그 앤 드롭")
        st.caption("아래 재료를 마우스로 끌어서 오른쪽에 떨어뜨리거나 클릭하여 선택하세요.")

        # HTML5 기반 마우스 드래그 앤 드롭 재료 선택기
        ing_list_html = "".join([f"<span class='ing-item' draggable='true' ondragstart='drag(event)' onclick='addIng(\"{ing}\")'>+ {ing}</span>" for ing in ALL_INGREDIENTS])
        
        drag_html = f"""
        <style>
            .ing-container {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; }}
            .ing-item {{
                background-color: #f0f2f6; border: 1px solid #ccc; padding: 6px 12px;
                border-radius: 16px; font-weight: bold; cursor: grab; user-select: none;
            }}
            .drop-zone {{
                border: 2px dashed #ff4b4b; background-color: #fff5f5;
                padding: 25px; border-radius: 12px; text-align: center;
                font-weight: bold; color: #ff4b4b; margin-top: 10px;
            }}
        </style>
        <div class="ing-container">
            {ing_list_html}
        </div>
        <div class="drop-zone" ondrop="drop(event)" ondragover="allowDrop(event)">
            📥 여기에 재료를 마우스로 끌어다 놓으세요 (Drag & Drop)
        </div>
        <script>
            function allowDrop(ev) {{ ev.preventDefault(); }}
            function drag(ev) {{ ev.dataTransfer.setData("text", ev.target.innerText.replace("+ ", "")); }}
            function drop(ev) {{
                ev.preventDefault();
                var data = ev.dataTransfer.getData("text");
                window.parent.postMessage({{type: 'ADD_ING', value: data}}, '*');
            }}
            function addIng(name) {{
                window.parent.postMessage({{type: 'ADD_ING', value: name}}, '*');
            }}
        </script>
        """
        components.html(drag_html, height=160)

        # 수동 선택 지원용 대체 선택창
        selected = st.multiselect("올려진 재료 목록 (여기서 직접 관리 가능):", ALL_INGREDIENTS, default=list(st.session_state.selected_ingredients))
        st.session_state.selected_ingredients = set(selected)

    with col_right:
        st.subheader("🔥 화덕 및 피자 판")
        
        current_set = st.session_state.selected_ingredients
        
        # 제출 판정용 백엔드 로직
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
            final_pizza_name = matched_pizza['name']
        elif len(current_set) > 0:
            final_pizza_name = "괴상한 피자"
        else:
            final_pizza_name = "도우 (빈 피자)"

        # 피자 이름을 굽기 전에 미리 노출하지 않도록 조치
        if st.session_state.baked:
            st.markdown(f"""
            <div class='oven-box'>
                🔴 화덕 내부 구이 완료! ♨️<br><br>
                <h3>[ 화덕에서 나온 피자 ]</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='pizza-box'>
                ⚪ 피자 도우 위 올려진 재료:<br>
                <b>{', '.join(st.session_state.selected_ingredients) if st.session_state.selected_ingredients else '없음'}</b><br><br>
                <h4>현재 상태: 도우 위 재료 조합 중...</h4>
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
                            st.toast(f"✅ 정답! [{final_pizza_name}] +{order['score']}점 획득!", icon="👏")
                        else:
                            st.session_state.score -= 1
                            st.toast(f"❌ 제출 실패! [{final_pizza_name}] 잘못된 피자입니다! -1점 감점!", icon="💥")
                    
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

    if diff == '쉬움':
        st.subheader(f"최종 획득 점수: **{score}점** (목표: 50점)")
        if score >= 50:
            st.balloons()
            st.success("🎉 축하합니다! 목표를 달성했습니다! 부자가 되어 돈이 펑펑 휘날립니다! 💵💶💷")
            st.markdown("# 🤑 💰 💸 💰 💸")
        else:
            st.error("😭 파산했습니다... 피자가게 문을 닫습니다. 💸")
            st.markdown("# 💸 🧎‍♂️ (털썩...)")

    elif diff == '어려움':
        st.subheader(f"최종 획득 점수: **{score}점** (목표: 100점)")
        if score >= 100:
            st.balloons()
            st.success("🎉 축하합니다! 100점 이상 달성! 부자가 되어 돈이 펑펑 휘날립니다! 💵💶💷")
            st.markdown("# 🤑 💰 💸 💰 💸")
        else:
            st.error("😭 파산했습니다... 목표 점수에 도달하지 못했습니다.")
            st.markdown("# 💸 🧎‍♂️ (털썩...)")

    elif diff == '한계':
        st.balloons()
        st.markdown(f"## 🎉 축하합니다! 당신은 **'{score}'** 의 점수를 획득했습니다!")
        st.info(f"🏆 최고 점수 기록: **{st.session_state.high_score}점**")

    st.divider()
    if st.button("🔄 다시 시작 (로비로 돌아가기)", type="primary"):
        st.session_state.page = 'lobby'
        st.rerun()
    
