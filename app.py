import streamlit as st
import pandas as pd
import plotly.express as px
from services.stock_api import get_quote, get_eod

st.set_page_config(page_title="US Stock Explorer", layout="wide")

st.title("📈 US Stock Explorer")

# ====================================
# SESSION STATE (watchlist)
# ====================================
if "tickers" not in st.session_state:
    st.session_state.tickers = ["AAPL"]


# ====================================
# ➕ ADD COMPANY UI
# ====================================
st.sidebar.header("➕ Add Company")

new_ticker = st.sidebar.text_input(
    "Enter US Stock Ticker",
    placeholder="e.g., MSFT"
)

if st.sidebar.button("Add to Watchlist"):
    if new_ticker:
        ticker = new_ticker.upper().strip()

        if ticker not in st.session_state.tickers:
            st.session_state.tickers.append(ticker)
            st.sidebar.success(f"{ticker} added!")
            st.rerun()
        else:
            st.sidebar.warning("Ticker already exists")


# ====================================
# 📌 WATCHLIST DISPLAY
# ====================================
st.sidebar.subheader("📌 Watchlist")

for t in st.session_state.tickers:
    col1, col2 = st.sidebar.columns([3, 1])

    with col1:
        st.write(t)

    with col2:
        if st.button("❌", key=f"remove_{t}"):
            st.session_state.tickers.remove(t)
            st.rerun()


# ====================================
# 📊 MAIN DASHBOARD
# ====================================
for symbol in st.session_state.tickers:

    st.divider()
    st.header(f"📊 {symbol}")

    # =====================
    # QUOTE SECTION
    # =====================
    quote_data = get_quote(symbol)

    if quote_data:
        q = quote_data[0]

        col1, col2, col3 = st.columns(3)

        col1.metric("Price", f"${q['price']}")
        col2.metric("Day High", f"${q['day_high']}")
        col3.metric("Day Low", f"${q['day_low']}")

    else:
        st.error(f"No quote data found for {symbol}")
        continue

    # =====================
    # HISTORICAL CHART
    # =====================
    hist_data = get_eod(symbol)

    if hist_data:
        df = pd.DataFrame(hist_data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        fig = px.line(
            df,
            x="date",
            y="close",
            title=f"{symbol} Historical Price"
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander(f"Show raw data ({symbol})"):
            st.dataframe(df)

    else:
        st.warning(f"No historical data found for {symbol}")
