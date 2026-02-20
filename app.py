import streamlit as st
import pandas as pd
import plotly.express as px
from services.stock_api import get_quote, get_eod

st.set_page_config(page_title="US Stock Explorer", layout="wide")

st.title("📈 US Stock Explorer")

# -------------------------
# ticker input
# -------------------------
symbol = st.text_input("Enter US Stock Ticker", "AAPL").upper()

if symbol:

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
        st.error("No quote data found")

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

        with st.expander("Show raw data"):
            st.dataframe(df)

    else:
        st.warning("No historical data found")