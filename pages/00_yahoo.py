import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Global Top 10 Market Cap Stocks", layout="wide")

st.title("📈 글로벌 시가총액 TOP 10 기업 주가 변화 (최근 1년)")

# 시가총액 TOP 10 기업 (2025년 기준, 수동 업데이트 가능)
top10_tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",   # 사우디 아람코 (타다울 거래소)
    "Nvidia": "NVDA",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "Eli Lilly": "LLY",
    "TSMC": "TSM"
}

# 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 데이터 다운로드
st.info("야후 파이낸스에서 데이터를 불러오는 중입니다. 잠시만 기다려주세요...")

data = {}
for name, ticker in top10_tickers.items():
    stock = yf.download(ticker, start=start_date, end=end_date)
    if not stock.empty:
        data[name] = stock["Adj Close"]

# 데이터프레임 결합
df = pd.DataFrame(data)

# 시각화
fig = go.Figure()
for company in df.columns:
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[company],
        mode='lines',
        name=company
    ))

fig.update_layout(
    title="📊 글로벌 시가총액 TOP10 기업의 최근 1년간 주가 변화",
    xaxis_title="날짜",
    yaxis_title="조정 종가 (USD)",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
