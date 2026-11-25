import streamlit as st
import random
import time

# ==========================================
# 1. 페이지 기본 설정
# ==========================================
st.set_page_config(
    page_title="3초밥! - 충북대 맛집 추천",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. 초기 식당 데이터 (팀원들과 실제 충북대 맛집으로 자유롭게 수정하세요!)
# ==========================================
INITIAL_RESTAURANTS = {
    "중문": [
        {"name": "또또와", "category": "분식", "menu": "즉석 떡볶이, 볶음밥"},
        {"name": "모퉁이 파스타", "category": "양식", "menu": "투움바 파스타, 리조또"},
        {"name": "이런이궈", "category": "중식", "menu": "마라탕, 꿔바로우"},
        {"name": "중문 돈까스", "category": "일식", "menu": "등심 돈까스, 냉모밀"},
        {"name": "개신 국밥", "category": "한식", "menu": "순대국밥, 수육백반"},
        {"name": "중문 김치찜", "category": "한식", "menu": "묵은지 돼지김치찜"},
        {"name": "사창동 텐동", "category": "일식", "menu": "새우 텐동, 온센타마고"},
        {"name": "중문 버거하우스", "category": "양식", "menu": "클래식 치즈버거 세트"},
    ],
    "정문": [
        {"name": "순돌이병천토종순대&수육국밥", "category": "한식", "menu": "순대국, 순대곱창전골(1인)"},
        {"name": "교촌치킨", "category": "양식", "menu": "허니 콤보, 레드콤보"},
        {"name": "대동 양꼬치", "category": "중식", "menu": "양꼬치, 양갈비살"},
        {"name": "로충칭 마라탕", "category": "중식", "menu": "마라탕, 마라샹궈"},
        {"name": "온오프피자", "category": "양식", "menu": "고르곤졸라피자, 페퍼로니피자"},
        {"name": "건방진김밥", "category": "분식", "menu": "치즈김밥, 떡볶이, 라면"},
    ],
    "서문": [
        {"name": "순돌이뚱글이순대", "category": "한식", "menu": "순대국밥"},
        {"name": "장군반점", "category": "중식", "menu": "간짜장, 짬뽕"},
        {"name": "서문 카츠", "category": "일식", "menu": "치즈 카츠, 카레 우동"},
        {"name": "원조또또만두찐빵만두", "category": "분식", "menu": "고기만두, 김치만두"},
        {"name": "꼬꼬맨치킨", "category": "양식", "menu": "양념치킨+후라이드"},
    ],
    "후문": [
        {"name": "후문 칼국수", "category": "한식", "menu": "바지락 칼국수, 왕만두"},
        {"name": "후문 카레집", "category": "일식", "menu": "치킨 가라아게 카레"},
        {"name": "후문 짬뽕", "category": "중식", "menu": "차돌 짬뽕, 볶음밥"},
        {"name": "후문 떡볶이", "category": "분식", "menu": "국물 떡볶이, 모듬튀김"},
        {"name": "후문 스테이크", "category": "양식", "menu": "부채살 스테이크 덮밥"},
    ],
}

CATEGORIES = ["한식", "중식", "일식", "양식", "분식"]

# ==========================================
# 3. 세션 상태 초기화 (화면 이동 & 데이터 유지)
# ==========================================
if "restaurants" not in st.session_state:
    # 깊은 복사로 초기 데이터 저장 (시연 중 제보한 가게가 실시간 추가됨)
    st.session_state.restaurants = {
        zone: [place.copy() for place in places]
        for zone, places in INITIAL_RESTAURANTS.items()
    }

if "reviews" not in st.session_state:
    st.session_state.reviews = {
        "또또와": ["가성비 최고! 공강 시간에 친구랑 가기 딱 좋아요."],
        "모퉁이 파스타": ["크림 소스가 꾸덕해서 맛있어요."],
    }

if "page" not in st.session_state:
    st.session_state.page = "main"  # main, select_mode, roulette, category, report, review
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "picked_place" not in st.session_state:
    st.session_state.picked_place = None
if "spin" not in st.session_state:
    st.session_state.spin = False
if "prev_page" not in st.session_state:
    st.session_state.prev_page = "main"

# ==========================================
# 4. PPT 시안 기반 커스텀 CSS 디자인
# ==========================================
st.markdown("""
<style>
/* 스트림릿 기본 상단바/푸터 숨겨서 실제 앱처럼 보이게 처리 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 전체 배경색 (부드러운 미색) */
.stApp {
    background-color: #F4F6F9;
}

/* 모바일 앱 화면 프레임 */
.block-container {
    max-width: 430px !important;
    min-height: 760px;
    background-color: #FFFFFF;
    border-radius: 28px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 12px 32px rgba(30, 64, 175, 0.08);
    padding: 2.2rem 1.6rem 2.5rem 1.6rem !important;
    margin-top: 1.5rem !important;
    margin-bottom: 2rem !important;
}

/* 메인 타이틀 디자인 */
.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    color: #4EA3DF;
    letter-spacing: -1px;
    margin-bottom: 4px;
    line-height: 1.15;
}
.main-subtitle {
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    color: #5DAEE6;
    margin-bottom: 28px;
}

/* 서브 페이지 상단 안내 문구 */
.page-heading {
    font-size: 23px;
    font-weight: 800;
    color: #1E293B;
    line-height: 1.38;
    margin-bottom: 22px;
    letter-spacing: -0.5px;
}
.highlight-blue {
    color: #3B95D9;
}

/* 일반 버튼 (PPT의 파스텔 블루 카드형 버튼) */
div.stButton > button {
    width: 100%;
    min-height: 58px;
    background: linear-gradient(90deg, #D9ECFA 0%, #EDF6FD 100%);
    color: #1E293B;
    border: 1px solid #CBE4F7;
    border-radius: 14px;
    font-size: 18px;
    font-weight: 700;
    box-shadow: 0 2px 6px rgba(78, 163, 223, 0.08);
    transition: all 0.2s ease;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #4EA3DF 0%, #72BCEE 100%);
    color: #FFFFFF;
    border-color: #4EA3DF;
    transform: translateY(-1px);
    box-shadow: 0 6px 14px rgba(78, 163, 223, 0.25);
}

/* 강조 버튼 (primary: 진한 하늘색 버튼 - '다시 돌리기', 선택된 항목 등) */
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #479CD9 0%, #68B7EC 100%);
    color: #FFFFFF;
    border: none;
    box-shadow: 0 6px 16px rgba(71, 156, 217, 0.35);
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(90deg, #3589C7 0%, #52A7E0 100%);
    color: #FFFFFF;
}

/* PPT 시안의 빛나는 파란 룰렛 박스 */
.roulette-wrapper {
    position: relative;
    margin: 26px 0 22px 0;
    padding-top: 14px;
}
.roulette-badge {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    background-color: #FFFFFF;
    padding: 2px 16px;
    font-size: 17px;
    font-weight: 800;
    color: #1E293B;
    white-space: nowrap;
    z-index: 2;
}
.roulette-box {
    background-color: #FFFFFF;
    border: 5px solid #67B4EA;
    border-radius: 22px;
    box-shadow: 0 0 22px rgba(86, 168, 228, 0.45);
    padding: 32px 16px 26px 16px;
    text-align: center;
}
.roulette-sub-item {
    font-size: 18px;
    font-weight: 600;
    color: #94A3B8;
    margin: 6px 0;
}
.roulette-main-item {
    font-size: 36px;
    font-weight: 900;
    color: #0F172A;
    margin: 8px 0;
    letter-spacing: -1px;
}
.roulette-detail {
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px dashed #CBD5E1;
    font-size: 14px;
    color: #475569;
}

/* 카테고리 리스트 식당 카드 */
.place-card {
    background: linear-gradient(135deg, #F4FAFF 0%, #FFFFFF 100%);
    border: 1.5px solid #CBE4F7;
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 3px 8px rgba(78, 163, 223, 0.07);
}
.place-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}
.place-name {
    font-size: 19px;
    font-weight: 800;
    color: #0F172A;
}
.place-tag {
    background-color: #4EA3DF;
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 999px;
}
.place-menu {
    font-size: 14px;
    color: #475569;
    margin-bottom: 4px;
}
.place-review {
    font-size: 13px;
    color: #2563EB;
    background-color: #EFF6FF;
    padding: 6px 10px;
    border-radius: 8px;
    margin-top: 8px;
}

/* 제보 버튼 강조용 구분선 */
.dashed-divider {
    border-top: 2px dashed #BCE0FA;
    margin: 22px 0 18px 0;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 보조 함수: 페이지 이동
# ==========================================
def go_to(page_name):
    st.session_state.prev_page = st.session_state.page
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 화면 1: 메인 화면 (기능 1 - 위치 선택)
# ==========================================
if st.session_state.page == "main":
    st.markdown('<div class="main-title">3초밥!</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">오늘은 어디서 밥먹지?</div>', unsafe_allow_html=True)

    zones = ["중문", "정문", "서문", "후문"]
    for idx, zone in enumerate(zones):
        # PPT 시안처럼 첫 번째(중문)를 포인트 컬러로 강조하고 나머지는 파스텔 블루
        btn_type = "primary" if idx == 0 else "secondary"
        if st.button(f"📍  {zone}  ›", key=f"zone_{zone}", type=btn_type, use_container_width=True):
            st.session_state.selected_zone = zone
            st.session_state.selected_category = None
            go_to("select_mode")

    st.markdown('<div class="dashed-divider"></div>', unsafe_allow_html=True)

    if st.button("📢  새로운 가게 제보  +", key="main_report_btn", use_container_width=True):
        go_to("report")

# ==========================================
# 화면 2: 기능 선택 (기능 2 룰렛 vs 기능 3 카테고리)
# ==========================================
elif st.session_state.page == "select_mode":
    zone = st.session_state.selected_zone
    count = len(st.session_state.restaurants[zone])

    st.markdown(
        f'<div class="page-heading">'
        f'<span class="highlight-blue">{zone}</span>에서 드신다고요?<br>'
        f'원하는 방식을 골라주세요!</div>',
        unsafe_allow_html=True
    )
    st.caption(f"현재 {zone} 구역에 등록된 검증 맛집: 총 {count}곳")

    st.write("")

    # 기능 2 진입 버튼
    if st.button("🎲  초간단 랜덤 룰렛 돌리기\n(3초 만에 딱 1곳 추천!)", key="go_roulette", type="primary", use_container_width=True):
        st.session_state.spin = True
        go_to("roulette")

    st.write("")

    # 기능 3 진입 버튼
    if st.button("🍽️  음식 종류별 식당 모아보기\n(한식·중식·일식·양식·분식)", key="go_category", use_container_width=True):
        st.session_state.selected_category = None
        go_to("category")

    st.markdown('<div class="dashed-divider"></div>', unsafe_allow_html=True)

    if st.button("⬅️  위치 다시 고르기", key="back_to_main_from_mode", use_container_width=True):
        go_to("main")

# ==========================================
# 화면 3-A: 기능 2 - 초간단 랜덤 룰렛 화면
# ==========================================
elif st.session_state.page == "roulette":
    zone = st.session_state.selected_zone
    places = st.session_state.restaurants[zone]

    st.markdown(
        f'<div class="page-heading">'
        f'<span class="highlight-blue">{zone}</span>에서 드신다고요?<br>'
        f'3초면 끝나요!</div>',
        unsafe_allow_html=True
    )

    roulette_placeholder = st.empty()

    # 룰렛 박스 HTML 생성 도우미
    def render_roulette_box(badge_text, top_name, mid_name, bot_name, detail_html=""):
        return (
            f'<div class="roulette-wrapper">'
            f'<div class="roulette-badge">{badge_text}</div>'
            f'<div class="roulette-box">'
            f'<div class="roulette-sub-item">{top_name}</div>'
            f'<div class="roulette-main-item">{mid_name}</div>'
            f'<div class="roulette-sub-item">{bot_name}</div>'
            f'{detail_html}'
            f'</div>'
            f'</div>'
        )

    # 룰렛 애니메이션 실행 (빠르게 돌다가 마지막에 천천히 멈춤)
    if st.session_state.spin and len(places) > 0:
        delays = [0.06] * 12 + [0.10, 0.14, 0.20, 0.28]
        total = len(places)
        current_idx = random.randint(0, total - 1)

        for delay in delays:
            current_idx = (current_idx + 1) % total
            prev_name = places[(current_idx - 1) % total]["name"]
            curr_name = places[current_idx]["name"]
            next_name = places[(current_idx + 1) % total]["name"]

            roulette_placeholder.markdown(
                render_roulette_box("밥집 롤링 중...", prev_name, curr_name, next_name),
                unsafe_allow_html=True
            )
            time.sleep(delay)

        # 최종 당첨 인덱스 저장
        final_idx = random.randint(0, total - 1)
        st.session_state.picked_place = {
            "index": final_idx,
            "data": places[final_idx]
        }
        st.session_state.spin = False

    # 멈춘 상태의 최종 결과 카드 표시
    if st.session_state.picked_place:
        total = len(places)
        idx = st.session_state.picked_place["index"] % total
        picked = st.session_state.picked_place["data"]
        prev_name = places[(idx - 1) % total]["name"]
        next_name = places[(idx + 1) % total]["name"]

        # 후기가 있으면 최신 후기 1개 표시
        place_reviews = st.session_state.reviews.get(picked["name"], [])
        review_snippet = f'<br>💬 "{place_reviews[-1]}"' if place_reviews else ""

        detail_html = (
            f'<div class="roulette-detail">'
            f'<b>[{picked["category"]}]</b> 대표 메뉴: {picked["menu"]}'
            f'{review_snippet}'
            f'</div>'
        )

        roulette_placeholder.markdown(
            render_roulette_box("🎉 오늘의 3초밥 픽!", prev_name, picked["name"], next_name, detail_html),
            unsafe_allow_html=True
        )

    # 다시 돌리기 버튼 (PPT 시안 핵심 버튼)
    if st.button("🎲  다시 돌리기", key="respin_btn", type="primary", use_container_width=True):
        st.session_state.spin = True
        st.rerun()

    st.write("")

    # 기능 4 버튼 (PPT 시안 하단 2개 버튼)
    if st.button("📢  새로운 가게 제보", key="roulette_report_btn", use_container_width=True):
        go_to("report")

    if st.button("✍️  다녀온 곳 후기 작성", key="roulette_review_btn", use_container_width=True):
        go_to("review")

    st.markdown('<div class="dashed-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍽️ 종류별 보기", key="switch_to_cat", use_container_width=True):
            go_to("category")
    with col2:
        if st.button("⬅️ 위치 변경", key="back_to_main_r", use_container_width=True):
            go_to("main")

# ==========================================
# 화면 3-B: 기능 3 - 카테고리별 단순 리스트 화면
# ==========================================
elif st.session_state.page == "category":
    zone = st.session_state.selected_zone
    places = st.session_state.restaurants[zone]

    st.markdown(
        f'<div class="page-heading">'
        f'<span class="highlight-blue">{zone}</span> 맛집 모아보기<br>'
        f'당기는 종류를 하나 골라주세요!</div>',
        unsafe_allow_html=True
    )

    # 카테고리 선택 버튼 (한 줄에 3개씩 깔끔하게 배치)
    cat_icons = {"한식": "🍚", "중식": "🥟", "일식": "🍣", "양식": "🍝", "분식": "🍢"}
    row1 = st.columns(3)
    row2 = st.columns(2)

    for i, cat in enumerate(CATEGORIES):
        target_col = row1[i] if i < 3 else row2[i - 3]
        is_selected = (st.session_state.selected_category == cat)
        with target_col:
            if st.button(
                f"{cat_icons[cat]} {cat}",
                key=f"cat_btn_{cat}",
                type="primary" if is_selected else "secondary",
                use_container_width=True
            ):
                st.session_state.selected_category = cat
                st.rerun()

    st.markdown('<div class="dashed-divider"></div>', unsafe_allow_html=True)

    # 카테고리를 선택했을 때 해당 지역 + 해당 카테고리 식당 전부 출력
    selected_cat = st.session_state.selected_category
    if selected_cat is None:
        st.info(f"👆 위에서 음식 종류를 하나 선택하면 **{zone}**의 모든 해당 식당을 보여드려요!")
    else:
        filtered = [p for p in places if p["category"] == selected_cat]
        st.markdown(f"**{zone} · {selected_cat} 식당 ({len(filtered)}곳)**")
        st.write("")

        if len(filtered) == 0:
            st.warning(f"아직 {zone}에 등록된 {selected_cat} 식당이 없어요. 알고 계신 맛집을 제보해 주세요!")
        else:
            for p in filtered:
                place_reviews = st.session_state.reviews.get(p["name"], [])
                review_html = (
                    f'<div class="place-review">💬 최근 후기: {place_reviews[-1]}</div>'
                    if place_reviews else ""
                )
                card_html = (
                    f'<div class="place-card">'
                    f'<div class="place-card-header">'
                    f'<span class="place-name">{p["name"]}</span>'
                    f'<span class="place-tag">{p["category"]}</span>'
                    f'</div>'
                    f'<div class="place-menu">🍴 대표 메뉴: {p["menu"]}</div>'
                    f'{review_html}'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

    st.write("")
    if st.button("🎲  못 고르겠어요! 랜덤 룰렛 돌리기", key="cat_to_roulette", type="primary", use_container_width=True):
        st.session_state.spin = True
        go_to("roulette")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📢 가게 제보", key="cat_report_btn", use_container_width=True):
            go_to("report")
    with col2:
        if st.button("⬅️ 위치 변경", key="back_to_main_c", use_container_width=True):
            go_to("main")

# ==========================================
# 화면 4-A: 기능 4 - 새로운 가게 제보 화면
# ==========================================
elif st.session_state.page == "report":
    st.markdown(
        '<div class="page-heading">'
        '📢 <span class="highlight-blue">새로운 맛집</span> 제보하기<br>'
        '나만의 찐맛집을 공유해주세요!</div>',
        unsafe_allow_html=True
    )

    default_zone_idx = 0
    zones = ["중문", "정문", "서문", "후문"]
    if st.session_state.selected_zone in zones:
        default_zone_idx = zones.index(st.session_state.selected_zone)

    with st.form("report_form"):
        r_zone = st.selectbox("위치 구역", zones, index=default_zone_idx)
        r_category = st.selectbox("음식 종류", CATEGORIES)
        r_name = st.text_input("식당 이름", placeholder="예: 충대 김치찌개")
        r_menu = st.text_input("대표 메뉴", placeholder="예: 돼지고기 김치찌개, 계란말이")
        submitted = st.form_submit_button("제보 등록하기", type="primary", use_container_width=True)

        if submitted:
            if not r_name.strip() or not r_menu.strip():
                st.error("식당 이름과 대표 메뉴를 모두 입력해 주세요!")
            else:
                st.session_state.restaurants[r_zone].append({
                    "name": r_name.strip(),
                    "category": r_category,
                    "menu": r_menu.strip()
                })
                st.success(f"🎉 [{r_zone}] '{r_name}' 식당이 3초밥에 바로 등록되었습니다!")

    if st.button("⬅️  돌아가기", key="back_from_report", use_container_width=True):
        go_to(st.session_state.prev_page)

# ==========================================
# 화면 4-B: 기능 4 - 다녀온 곳 후기 작성 화면
# ==========================================
elif st.session_state.page == "review":
    st.markdown(
        '<div class="page-heading">'
        '✍️ <span class="highlight-blue">다녀온 곳</span> 한 줄 후기<br>'
        '솔직한 후기를 남겨주세요!</div>',
        unsafe_allow_html=True
    )

    zone = st.session_state.selected_zone or "중문"
    zone_place_names = [p["name"] for p in st.session_state.restaurants[zone]]

    # 방금 룰렛에서 뽑힌 가게가 기본 선택되도록 설정
    default_idx = 0
    if st.session_state.picked_place and st.session_state.picked_place["data"]["name"] in zone_place_names:
        default_idx = zone_place_names.index(st.session_state.picked_place["data"]["name"])

    with st.form("review_form"):
        target_name = st.selectbox(f"{zone} 식당 선택", zone_place_names, index=default_idx)
        review_text = st.text_area("한 줄 후기", placeholder="예: 양 많고 사장님이 친절해요! 점심 피크 시간엔 조금 일찍 가는 걸 추천")
        submitted = st.form_submit_button("후기 등록하기", type="primary", use_container_width=True)

        if submitted:
            if not review_text.strip():
                st.error("후기 내용을 입력해 주세요!")
            else:
                st.session_state.reviews.setdefault(target_name, []).append(review_text.strip())
                st.success(f"💬 '{target_name}'에 소중한 후기가 등록되었습니다!")

    if st.button("⬅️  돌아가기", key="back_from_review", use_container_width=True):
        go_to(st.session_state.prev_page)