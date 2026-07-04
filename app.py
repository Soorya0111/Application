import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Stock Price Viewer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Price Viewer")
st.write("Fetch stock price data from Yahoo Finance.")

# --------------------------
# User Input
# --------------------------

ticker = st.text_input(
    "Enter Stock Symbol",
    value="RELIANCE.NS"
).strip().upper()

period = st.selectbox(
    "Select Time Period",
    (
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max",
    ),
)

interval_mapping = {
    "1mo": "1d",
    "3mo": "1d",
    "6mo": "1d",
    "1y": "1d",
    "2y": "1d",
    "5y": "1wk",
    "10y": "1wk",
    "max": "1mo",
}

interval = interval_mapping[period]

# --------------------------
# Fetch Data
# --------------------------

if st.button("Fetch Data"):

    if ticker == "":
        st.warning("Please enter a stock symbol.")
        st.stop()

    with st.spinner("Downloading data..."):

        try:
            df = yf.download(
                tickers=ticker,
                period=period,
                interval=interval,
                auto_adjust=True,
                progress=False,
                threads=False,
            )

        except Exception as e:
            st.error(f"Error downloading data:\n\n{e}")
            st.stop()

    if df.empty:
        st.error("No data found for this ticker.")
        st.stop()

    # --------------------------------------------------
    # Fix MultiIndex returned by newer yfinance versions
    # --------------------------------------------------
    if df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)

    if "Close" not in df.columns:
        st.error("Close price data not available.")
        st.stop()

    close = df["Close"].astype(float)

    st.subheader(f"{ticker} Price Data")

    st.dataframe(df.tail())

    # --------------------------
    # Plot
    # --------------------------

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        close.index,
        close.values,
        linewidth=2,
        color="blue",
    )

    ax.set_title(f"{ticker} Closing Price ({period})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.grid(True)

    st.pyplot(fig)

    # --------------------------
    # Metrics
    # --------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Latest Close",
        f"{close.iloc[-1]:,.2f}"
    )

    col2.metric(
        "Highest Close",
        f"{close.max():,.2f}"
    )

    col3.metric(
        "Lowest Close",
        f"{close.min():,.2f}"
    )
