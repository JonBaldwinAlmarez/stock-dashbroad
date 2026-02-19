import streamlit as st
from services.stock_api import get_stock_quote, get_historical_data
from utils.analysis import to_dataframe, calculate_moving_average
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📊 Stock Analysis Dashboard")

# Input section
symbol = st.text_input("Enter Stock Ticker", "AAPL").upper()
days = st.slider("Number of Historical Days", 5, 90, 30)
analyze = st.button("Analyze")

if analyze and symbol:
    # Current price
    quote = get_stock_quote(symbol)
    if quote:
        st.metric(label=f"{symbol} Current Price", value=f"${quote['price']:.2f}", delta=f"{quote['change_percent']:.2f}%")
    else:
        st.error("Failed to fetch stock quote")

    # Historical data
    historical = get_historical_data(symbol, days)
    df = to_dataframe(historical)
    df = calculate_moving_average(df, window=5)

    if not df.empty:
        st.subheader(f"📈 {symbol} Price Chart")
        fig = px.line(df, y='c', title=f"{symbol} Closing Price", labels={'c':'Close'})
        fig.add_scatter(x=df.index, y=df.get('MA_5'), mode='lines', name='MA 5')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Data Table")
        st.dataframe(df)
    else:
        st.warning("No historical data found.")
