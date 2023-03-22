import streamlit as st
import requests
import pandas as pd
import time

# Set API endpoint and headers
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin",
    "vs_currencies": "usd"
}

# Define function to get BTC price
def get_btc_price():
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    else:
        data = response.json()
        return data["bitcoin"]["usd"]

# Display BTC price in real-time
st.write("# Real-Time BTC Price")
while True:
    price = get_btc_price()
    if price:
        st.write(f"BTC price: {price} USD")
    else:
        st.error("Failed to retrieve BTC price from CoinGecko API - check your internet connection.")
    time.sleep(5)
