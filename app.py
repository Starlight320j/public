import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="득근득근 운동일지",
    page_icon="🏋️‍♂️",
    layout="wide"
)

# --- 2. 데이터 관리 (Session State) ---
# 앱이 새로고침되어도 데이터가 유지되도록 session_state 사용
if 'workout_schedule' not in st.session_state:
    # 예시 데이터 초기화
    st.session_state.workout_schedule = [
        {"요일": "월", "부위": "가슴", "운동명": "벤치프레스", "무게(kg)": 60, "세트": 4, "횟수": 10, "완료": False},
        {"요일": "월", "부위": "삼두", "운동명": "케이블 푸쉬다운", "무게(kg)": 25, "세트": 3, "횟수": 12, "완료": False},
        {"요일": "화", "부위": "등", "운동명": "데드리프트", "무게(kg)": 80, "세트": 5, "횟수": 5, "완료": False},
    ]

# --- 3. 사이드바: 운동 추가하기 ---
st.sidebar.header("➕ 운동 루틴 추가")

days_option = ["월", "화", "수", "목", "금", "토", "일"]
parts_option = ["가슴", "등", "하체", "어깨", "이두", "삼두", "복근", "유산소"]

with st.sidebar.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    s_day = col1.selectbox("요일 선택", days_option)
    s_part = col2.selectbox("타겟 부위", parts_option)
    
    s_name = st.text_input("운동명 (예: 스쿼트)")
    
    col3, col4, col5 = st.columns(3)
    s_weight = col3.number_input("무게(kg)", min_value=0, value=20, step=5)
    s_sets = col4.number_input("세트 수", min_value=1, value=3)
    s_reps = col5.number_input("횟수", min_value=1, value=10)
    
    submit_btn = st.form_submit_button("루틴에 추가하기")
    
    if submit_btn and s_name:
        new_workout = {
            "요일": s_day,
            "부위": s_part,
            "운동명": s_name,
            "무게(kg)": s_weight,
            "세트": s_sets,
            "횟수": s_reps,
            "완료": False
        }
        st.session_state.workout_schedule.append(new_workout)
        st.success(f"{s_day}요일 루틴에 '{s_name}' 추가 완료!")

# --- 4. 메인 화면: 내 운동 일정표 ---
st.title("🏋️‍♂️ 주간 웨이트 트레이닝 일정표")
st.markdown("이번 주 목표를 확인하고 운동을 기록해보세요!")

# 데이터프레임 변환
df = pd.DataFrame(st.session_state.workout_schedule)

# 탭으로 요일 구분
tabs = st.tabs(days_option)

for i, day in enumerate(days_option):
    with tabs[i]:
        # 해당 요일의 데이터만 필터링
        day_schedule = df[df["요일"] == day]
        
        if day_schedule.empty:
            st.info(f"{day}요일은 휴식일이거나 등록된 운동이 없습니다. 푹 쉬세요! 🛌")
        else:
            st.subheader(f"📅 {day}요일 운동 리스트")
            
            # 리스트 형태로 출력 (체크박스 기능 포함)
            for idx, row in day_schedule.iterrows():
                # 고유한 키(key) 생성을 위해 인덱스 활용
                col_check, col_info = st.columns([1, 10])
                
                with col_check:
                    # 실제 데이터베이스 연동이 없으므로 UI상 체크만 가능하게 구현
                    is_checked = st.checkbox("", key=f"{day}_{idx}")
                
                with col_info:
                    style = "text-decoration: line-through; color: gray;" if is_checked else ""
                    st.markdown(
                        f"<div style='{style} font-size:18px;'>"
                        f"<b>[{row['부위']}] {row['운동명']}</b> | "
                        f"{row['무게(kg)']}kg X {row['세트']}세트 X {row['횟수']}회"
                        f"</div>", 
                        unsafe_allow_html=True
                    )

# --- 5. 전체 일정 한눈에 보기 (하단) ---
st.divider()
with st.expander("📋 전체 루틴 표로 보기 (클릭하여 펼치기)"):
    if not df.empty:
        # 보기 좋게 컬럼 순서 정렬
        display_df = df[["요일", "부위", "운동명", "무게(kg)", "세트", "횟수"]]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        if st.button("모든 기록 초기화 (주의)"):
            st.session_state.workout_schedule = []
            st.rerun()
    else:
        st.write("등록된 운동이 없습니다.")
