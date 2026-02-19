import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="기후변화와 생물다양성",
    page_icon="🌿",
    layout="wide"
)

# --- 2. 데이터 로드 (모의 데이터 생성) ---
@st.cache_data
def load_data():
    # 1980년부터 2024년까지의 데이터 생성
    years = np.arange(1980, 2025)
    n = len(years)
    
    # 기온: 점차 상승하는 추세 + 랜덤 변동
    temperature = 14.0 + (years - 1980) * 0.04 + np.random.normal(0, 0.2, n)
    
    # 생물다양성 지수: 기온이 오를수록 감소하는 역상관관계 설정
    bio_index = 100 - (years - 1980) * 0.8 + np.random.normal(0, 2, n)
    
    return pd.DataFrame({
        "Year": years,
        "Temperature": temperature,
        "Biodiversity": bio_index
    })

df = load_data()

# --- 3. 사이드바 (사용자 컨트롤) ---
st.sidebar.header("🔍 분석 옵션")
st.sidebar.write("분석할 기간을 선택하세요.")
year_range = st.sidebar.slider("연도 범위", 1980, 2024, (1990, 2024))

# 데이터 필터링
filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# --- 4. 메인 대시보드 레이아웃 ---
st.title("🌍 기후변화에 따른 생물다양성 위기")
st.markdown("""
이 대시보드는 **지구 온난화(기온 상승)**가 **생물다양성 감소**에 미치는 잠재적 영향을 시각화합니다.
데이터는 시뮬레이션된 예시입니다.
""")

st.divider()

# KPI 메트릭 (주요 지표 표시)
col1, col2, col3 = st.columns(3)

start_temp = filtered_df["Temperature"].iloc[0]
end_temp = filtered_df["Temperature"].iloc[-1]
temp_change = end_temp - start_temp

start_bio = filtered_df["Biodiversity"].iloc[0]
end_bio = filtered_df["Biodiversity"].iloc[-1]
bio_change = end_bio - start_bio

col1.metric("평균 기온 변화", f"{end_temp:.1f} °C", f"{temp_change:+.1f} °C", delta_color="inverse")
col2.metric("생물다양성 지수", f"{int(end_bio)}", f"{int(bio_change)}", delta_color="normal") # normal은 감소 시 빨간색
col3.metric("분석 기간", f"{year_range[1] - year_range[0]} 년")

# --- 5. 차트 시각화 (이중 축 그래프) ---
st.subheader("📈 기온 상승 vs 생물다양성 감소 추이")

# Plotly로 이중 축 차트 생성
fig = go.Figure()

# 기온 (왼쪽 Y축)
fig.add_trace(go.Scatter(
    x=filtered_df["Year"], 
    y=filtered_df["Temperature"],
    name="평균 기온 (°C)",
    line=dict(color="#FF5733", width=3)
))

# 생물다양성 (오른쪽 Y축)
fig.add_trace(go.Bar(
    x=filtered_df["Year"], 
    y=filtered_df["Biodiversity"],
    name="생물다양성 지수",
    yaxis="y2",
    marker=dict(color="#2E86C1", opacity=0.4)
))

# 레이아웃 업데이트 (축 설정)
fig.update_layout(
    xaxis=dict(title="연도"),
    yaxis=dict(title="기온 (°C)", titlefont=dict(color="#FF5733"), tickfont=dict(color="#FF5733")),
    yaxis2=dict(
        title="생물다양성 지수",
        titlefont=dict(color="#2E86C1"),
        tickfont=dict(color="#2E86C1"),
        overlaying="y",
        side="right"
    ),
    hovermode="x unified",
    legend=dict(x=0, y=1.1, orientation="h")
)

st.plotly_chart(fig, use_container_width=True)

# --- 6. 상관관계 산점도 ---
st.subheader("🔗 상관관계 분석")
col_chart1, col_text1 = st.columns([2, 1])

with col_chart1:
    fig_corr = px.scatter(
        filtered_df, 
        x="Temperature", 
        y="Biodiversity", 
        trendline="ols", # 추세선 추가
        labels={"Temperature": "기온", "Biodiversity": "생물다양성"},
        color_discrete_sequence=["green"]
    )
    st.plotly_chart(fig_corr, use_container_width=True)

with col_text1:
    st.info("""
    **해석 가이드:**
    
    좌측 그래프의 추세선이 **우하향**한다면, 기온이 높을수록 생물다양성이 낮아진다는 **음의 상관관계**를 의미합니다.
    
    이는 서식지 파괴나 환경 스트레스로 인한 종 감소를 시사할 수 있습니다.
    """)
