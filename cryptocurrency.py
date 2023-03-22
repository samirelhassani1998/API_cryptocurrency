import streamlit as st
import requests
import pandas as pd
import numpy as np
import time

# Set API endpoint and headers
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "c7271d78-54dd-4159-8409-6486b5f01e27"
}

# Set parameters for API request
params = {
    "symbol": "BTC",
    "convert": "USD"
}

# Function to make API request and retrieve price data
def get_btc_price():
    response = requests.get(url, headers=headers, params=params)
    data = response.json()["data"]["BTC"]
    price = data["quote"]["USD"]["price"]
    return price

# Streamlit app
st.title("Current BTC Price")
price = get_btc_price()
st.write(f"Current BTC price is {price:.2f} USD")

# Streamlit app loop to update price every minute
while True:
    time.sleep(60)
    price = get_btc_price()
    st.write(f"Current BTC price is {price:.2f} USD")
