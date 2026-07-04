import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Stock Price Chart",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Price Viewer")
st.write("Fetch stock data from Yahoo Finance and visualize it.")

# -------------------------
# User Inputs
# -------------------------

ticker = st.text_input(
    "Enter Stock Symbol",
    value="RELIANCE.NS"
)

period = st.selectbox(
    "Select Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max"
    ]
)

interval_mapping = {
    "1mo": "1d",
    "3mo": "1d",
    "6mo": "1d",
    "1y": "1d",
    "2y": "1d",
    "5y": "1wk",
    "10y": "1wk",
    "max": "1mo"
}

interval = interval_mapping[period]

# -------------------------
# Download Data
# -------------------------

if st.button("Fetch Data"):

    with st.spinner("Downloading data..."):

        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True
        )

    if df.empty:
        st.error("No data found.")
    else:

        st.subheader("Price Data")

        st.dataframe(df.tail())

        fig, ax = plt.subplots(figsize=(12,5))

        ax.plot(
            df.index,
            df["Close"],
            linewidth=2
        )

        ax.set_title(f"{ticker} Closing Price ({period})")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")

        ax.grid(True)

        st.pyplot(fig)

        st.metric(
            "Latest Close",
            f"{df['Close'].iloc[-1]:.2f}"
        )

        st.metric(
            "Highest Close",
            f"{df['Close'].max():.2f}"
        )

        st.metric(
            "Lowest Close",
            f"{df['Close'].min():.2f}"
        )
