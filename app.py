import streamlit as st
import pandas as pd
import requests
import time

# Streamlit page setup
st.set_page_config(page_title="Crypto Price Tracker", page_icon="💹", layout="wide")
st.title("💹 Real-Time Crypto Price Tracker")

st.write("Track live cryptocurrency prices and market data using the CoinGecko API.")

# Sidebar options
st.sidebar.header("⚙️ Settings")
refresh_rate = st.sidebar.slider("Auto-refresh every (seconds):", 5, 60, 15)
num_coins = st.sidebar.slider("Number of coins to display:", 5, 50, 10)

# Fetch data from CoinGecko API
@st.cache_data(ttl=refresh_rate)
def get_crypto_data(limit):
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False,
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)[["id", "symbol", "current_price", "price_change_percentage_24h", "market_cap"]]
    df.rename(columns={
        "id": "Name",
        "symbol": "Symbol",
        "current_price": "Current Price (USD)",
        "price_change_percentage_24h": "24h Change (%)",
        "market_cap": "Market Cap (USD)"
    }, inplace=True)
    return df

# Auto-refresh functionality
placeholder = st.empty()
while True:
    with placeholder.container():
        df = get_crypto_data(num_coins)

        # Color formatting
        def color_change(val):
            color = 'green' if val > 0 else 'red'
            return f'color: {color}; font-weight: bold'

        st.dataframe(df.style.format({
            "Current Price (USD)": "${:,.2f}",
            "Market Cap (USD)": "${:,.0f}",
            "24h Change (%)": "{:.2f}%"
        }).applymap(color_change, subset=["24h Change (%)"]))

        st.caption("Data fetched from CoinGecko API")

    time.sleep(refresh_rate)
