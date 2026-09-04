import streamlit as st
import random
import time

# 페이지 기본 설정
st.set_page_config(page_title="화덕 피자 타이쿤", page_icon="🍕", layout="wide")

# UI 커스텀 스타일링
st.markdown("""
<style>
    .stApp {
        background-color: #FFF9F2;
        color: #2D3748;
    }
    
    h1, h2, h3, h4, h5, h6, p, label {
        color: #2D3748 !important;
        font-family: 'Pretendard', sans-serif;
    }
    
    .dashboard-text span, .dashboard-text div {
        color: inherit !important;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        font-size: 15px;
        background-color: #FFFFFF;
        border: 2px solid #E2E8F0;
        color: #2D3748 !important;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.04);
        transition: all 0.2s ease-in-out;
        padding: 8px 12px;
    }
    .stButton>button:hover {
        border-color: #DD6B20;
        color: #DD6B20 !important;
        transform: translateY(-2px);
        box-shadow: 0px 6px 12px rgba(221, 107, 32, 0.15);
    }
    
    .custom-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #EDF2F7;
        margin-bottom: 15px;
    }
    
    .hidden-card {
        background: linear-gradient(135deg, #FFF5F5 0%, #FED7D7 100%);
        border-radius: 16px;
        padding: 20px;
        border: 2px dashed #E53E3E;
        box-shadow: 0px 4px 12px rgba(229, 62, 62, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 이미지 URL 정의
# ---------------------------------------------------------
# 1. 로비 화면 (안정적인 고화질 URL)
LOBBY_BANNER_URL = "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=1000&auto=format&fit=crop&q=80"

# 2. 플레이 화면 (이전 핀터레스트 원본 이미지)
PLAY_DOUGH_URL = "https://i.pinimg.com/736x/87/a2/27/87a227361956dd96bce78d8ca49d4be2.jpg"

# 3. 기타 배경 및 결과 화면 이미지
OVEN_IMG_URL = "https://images.unsplash.com/photo-1541745537411-b8046dc6d66c?w=500&auto=format&fit=crop&q=80"
BANKRUPT_IMG_URL = "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=500&auto=format&fit=crop&q=80"
RICH_IMG_URL = "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=500&auto=format&fit=crop&q=80"
LIMIT_SUCCESS_URL = "https://images.unsplash.com/photo-1531545514256-b1400bc00f31?w=500&auto=format&fit=crop&q=80"

# ---------------------------------------------------------
# 데이터 정의 (모든 피자 점수 +5점 적용)
# ---------------------------------------------------------
INGREDIENT_ICONS = {
    "케첩": "🥫", "치즈": "🧀", "파": "🧅", "페퍼로니": "🍕",
    "버섯": "🍄", "불고기": "🥩", "감자": "🥔", "고구마": "🍠",
    "사과": "🍎", "복숭아": "🍑", "파인애플": "🍍", "꿀": "🍯"
}

ALL_INGREDIENTS = [
    "케첩", "치즈", "파", "페퍼로니", 
    "버섯", "불고기", "감자", "고구마", 
    "사과", "복숭아", "파인애플", "꿀"
]

PIZZA_RECIPES = [
    {"name": "파피자", "score": 8, "ingredients": {"파", "케첩", "치즈"}},
    {"name": "버섯피자", "score": 8, "ingredients": {"버섯", "케첩", "치즈"}},
    {"name": "페퍼로니피자", "score": 8, "ingredients": {"페퍼로니", "케첩", "치즈"}},
    {"name": "치즈피자", "score": 8, "ingredients": {"케첩", "치즈"}},
    {"name": "피자", "score": 8, "ingredients": {"케첩"}},
    {"name": "감자피자", "score": 8, "ingredients": {"감자", "케첩", "치즈"}},
    {"name": "고구마피자", "score": 8, "ingredients": {"고구마", "케첩", "치즈"}},
    {"name": "사과피자", "score": 8, "ingredients": {"사과", "케첩", "치즈"}},
    {"name": "복숭아피자", "score": 8, "ingredients": {"복숭아", "케첩", "치즈"}},
    {"name": "불고기버섯피자", "score": 9, "ingredients": {"불고기", "버섯", "케첩", "치즈"}},
    {"name": "페퍼로니버섯피자", "score": 9, "ingredients": {"페퍼로니", "버섯", "케첩", "치즈"}},
    {"name": "감자페퍼로니피자", "score": 10, "ingredients": {"치즈", "케첩", "페퍼로니", "감자"}},
    {"name": "슈프림피자", "score": 10, "ingredients": {"케첩", "페퍼로니", "불고기", "버섯", "파"}},
    {"name": "고르곤졸라피자", "score": 10, "ingredients": {"꿀", "치즈", "복숭아", "고구마", "사과", "파인애플"}},
    {"name": "하와이안피자", "score": 10, "ingredients": {"치즈", "케첩", "파인애플", "페퍼로니"}},
    {"name": "콤비네이션피자", "score": 11, "ingredients": {"치즈", "케첩", "페퍼로니", "불고기", "버섯", "파"}},
]

HIDDEN_RECIPES = [
    {"name": "슈퍼 콤비네이션 피자", "score": 14, "ingredients": set(ALL_INGREDIENTS), "id": 1, "hint": "모든 재료가 전부 들어간 완벽한 피자!"},
    {"name": "과일피자", "score": 12, "ingredients": {"사과", "복숭아", "파인애플"}, "id": 2, "hint": "달콤한 과일들만 모아 만든 피자!"}
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
    st.markdown("<h1 style='text-align: center; font-size: 42px;'>🍕 화덕 피자 타이쿤</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #718096 !important; font-size: 18px;'>최고의 셰프가 되어 최고의 피자를 만들어보세요!</p>", unsafe_allow_html=True)
    
    st.image(LOBBY_BANNER_URL, use_container_width=True)
    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.subheader("📋 레시피 공부")
        st.write("다양한 피자 조합을 미리 숙지하세요!")
        if st.button("📖 주문표 열기"):
            st.session_state.page = 'menu'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.subheader("⚙️ 난이도 설정")
        selected_diff = st.radio(
            "난이도 선택", 
            ["쉬움", "어려움", "한계"], 
            index=["쉬움", "어려움", "한계"].index(st.session_state.difficulty)
        )
        st.session_state.difficulty = selected_diff
        
        if selected_diff == "쉬움":
            st.info("💡 **쉬움**: 턴당 20초 / 목표 50점")
        elif selected_diff == "어려움":
            st.warning("🔥 **어려움**: 턴당 10초 / 목표 100점")
        else:
            st.error("💀 **한계**: 턴당 10초 / 무제한 점수 도전")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.subheader("🔥 영업 시작")
        st.write("제한 시간 **120초** 동안 주문을 처리하세요.")
        if st.button("🚀 게임 시작하기"):
            start_game()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 페이지 2: 주문표 화면
# ---------------------------------------------------------
elif st.session_state.page == 'menu':
    st.title("📜 피자 레시피 주문표")
    if st.button("⬅️ 로비로 돌아가기"):
        st.session_state.page = 'lobby'
        st.rerun()
    st.divider()
    
    st.subheader("🍕 일반 레시피")
    cols = st.columns(2)
    for idx, pizza in enumerate(PIZZA_RECIPES):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class='custom-card'>
                <h3 style='margin-top:0;'>{pizza['name']} <span style='color:#DD6B20; font-size:16px;'>(+{pizza['score']}점)</span></h3>
                <p><b>필요 재료:</b> {', '.join(pizza['ingredients'])}</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.subheader("✨ 히든 피자 레시피 (비밀 레시피)")
    h_cols = st.columns(2)
    for idx, hidden in enumerate(HIDDEN_RECIPES):
        with h_cols[idx % 2]:
            st.markdown(f"""
            <div class='hidden-card'>
                <h3 style='margin-top:0; color:#C53030 !important;'>🔒 {hidden['name']} <span style='font-size:16px;'>(+{hidden['score']}점)</span></h3>
                <p><b>필요 재료:</b> <span style='color:#E53E3E; font-weight:bold;'>❓❓❓ (숨겨진 조합)</span></p>
                <p style='font-size:13px; color:#718096 !important;'>💡 힌트: {hidden['hint']}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 페이지 3: 게임 플레이 화면
# ---------------------------------------------------------
elif st.session_state.page == 'game':
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

    st.markdown(f"""
    <div class="dashboard-text" style="
        border-radius: 16px; 
        padding: 18px; 
        background: linear-gradient(135deg, #FF7E5F 0%, #FEB47B 100%); 
        box-shadow: 0px 6px 16px rgba(255, 126, 95, 0.3); 
        margin-bottom: 25px;
    ">
        <div style="display: flex; justify-content: space-around; align-items: center; font-size: 18px; font-weight: 800; color: #FFFFFF !important;">
            <div>🛎️ 주문: <span style="font-size: 22px; color: #FFF066 !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">{order['name']}</span></div>
            <div>⏱️ 남은시간: <span style="font-size: 22px; color: #FFFFFF !important;">{remaining_game}초</span></div>
            <div>⏳ 턴시간: <span style="font-size: 22px; color: #FFFFFF !important;">{remaining_turn}초</span></div>
            <div>⭐ 점수: <span style="font-size: 22px; color: #FFF066 !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">{st.session_state.score}점</span></div>
            <div>🎯 목표: <span style="font-size: 22px; color: #FFFFFF !important;">{target_score}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    main_col1, main_col2 = st.columns(2)

    with main_col1:
        selected_list = list(st.session_state.selected_ingredients)
        ing_display = " ".join([INGREDIENT_ICONS[ing] for ing in selected_list]) if selected_list else "빈 도우"
        baked_status = "♨️ 노릇노릇 구워짐!" if st.session_state.baked else "⚪ 토핑 올리는 중"
        
        st.markdown(f"""
        <div style="text-align: center;" class="custom-card">
            <h4 style="margin-bottom: 10px;">🥣 도우 상태</h4>
            <div style="
                width: 230px; height: 230px; border-radius: 50%;
                background-image: url('{PLAY_DOUGH_URL}'); background-size: cover; background-position: center;
                border: 6px solid #CBD5E0; margin: 0 auto; display: flex; flex-direction: column;
                justify-content: center; align-items: center; box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
            ">
                <div style="background: rgba(0,0,0,0.7); padding: 8px 16px; border-radius: 20px; color: white !important; font-size: 22px; max-width: 90%;">
                    {ing_display}
                </div>
            </div>
            <p style="margin-top: 12px; font-weight: bold; color: {'#E53E3E' if st.session_state.baked else '#319795'} !important;">{baked_status}</p>
        </div>
        """, unsafe_allow_html=True)

    with main_col2:
        st.markdown(f"""
        <div style="text-align: center;" class="custom-card">
            <h4 style="margin-bottom: 10px;">🔥 이탈리아 화덕</h4>
            <div style="
                width: 230px; height: 230px; border-radius: 50%;
                background-image: url('{OVEN_IMG_URL}'); background-size: cover; background-position: center;
                border: 6px solid #DD6B20; margin: 0 auto; box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
            ">
            </div>
            <p style="margin-top: 12px; font-weight: bold; color: #718096 !important;">섭씨 400도 유지 중</p>
        </div>
        """, unsafe_allow_html=True)

    col_bottom_left, col_bottom_right = st.columns([2, 1])

    with col_bottom_right:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ 조작하기")
        
        if st.button("🔥 화덕에 굽기", use_container_width=True):
            st.session_state.baked = True
            st.toast("피자를 화덕에 구웠습니다!", icon="🔥")
            st.rerun()

        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("📤 제출", use_container_width=True):
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
                                st.toast(f"✨ 히든 피자({h['name']}) 완성! +{h['score']}점!", icon="🎉")
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
        st.markdown("</div>", unsafe_allow_html=True)

    with col_bottom_left:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 🛒 재료 올리기")
        
        grid_cols = st.columns(4)
        for idx, ing in enumerate(ALL_INGREDIENTS):
            with grid_cols[idx % 4]:
                is_selected = ing in st.session_state.selected_ingredients
                btn_label = f"{INGREDIENT_ICONS[ing]} {ing} {'✅' if is_selected else ''}"
                
                if st.button(btn_label, key=f"ing_btn_{ing}"):
                    if is_selected:
                        st.session_state.selected_ingredients.remove(ing)
                    else:
                        st.session_state.selected_ingredients.add(ing)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 페이지 4: 결과 화면
# ---------------------------------------------------------
elif st.session_state.page == 'result':
    st.markdown("<h1 style='text-align: center;'>🏁 영업 종료 - 결과 발표</h1>", unsafe_allow_html=True)
    st.divider()

    score = st.session_state.score
    diff = st.session_state.difficulty

    if score > st.session_state.high_score:
        st.session_state.high_score = score

    st.markdown("<div class='custom-card' style='text-align:center;'>", unsafe_allow_html=True)
    
    if diff == '쉬움':
        st.subheader(f"최종 점수: {score}점 / 목표 점수: 50점")
        if score >= 50:
            st.image(RICH_IMG_URL, width=350)
            st.balloons()
            st.success("🎉 목표 달성 성공! 대박 난 피자집 사장님이 되었습니다! 💵")
        else:
            st.image(BANKRUPT_IMG_URL, width=350)
            st.error("😭 목표 달성 실패... 가게가 파산했습니다.")

    elif diff == '어려움':
        st.subheader(f"최종 점수: {score}점 / 목표 점수: 100점")
        if score >= 100:
            st.image(RICH_IMG_URL, width=350)
            st.balloons()
            st.success("🎉 목표 달성 성공! 억만장자 피자 장인 등장! 💵")
        else:
            st.image(BANKRUPT_IMG_URL, width=350)
            st.error("😭 실패... 적자를 이겨내지 못하고 파산했습니다.")

    elif diff == '한계':
        st.image(LIMIT_SUCCESS_URL, width=350)
        st.balloons()
        st.markdown(f"<h2>🔥 한계 도전 최고 점수: <span style='color:#E53E3E;'>{score}점</span></h2>", unsafe_allow_html=True)
        st.info("축하합니다! 당신의 한계를 뛰어넘었습니다! 🏆")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 로비로 돌아가기", use_container_width=True):
        st.session_state.page = 'lobby'
        st.rerun()
