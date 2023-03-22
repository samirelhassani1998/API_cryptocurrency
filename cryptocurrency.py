import streamlit as st
import requests
import pandas as pd
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt

# Set API endpoint and headers
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "c7271d78-54dd-4159-8409-6486b5f01e27"
}
symbol = "BTC"
convert = "USD"

# Time interval in seconds
time_interval = 5

# Set up empty lists for timestamp and price data
timestamps = []
prices = []

# Set up plot
fig, ax = plt.subplots()
ax.set_title("BTC/USD Price")

# Main program loop
while True:
    # Make API request
    params = {"symbol": symbol, "convert": convert}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        st.error("Failed to retrieve data from CoinMarketCap API - check your API Key and try again.")
        break
    data = response.json()["data"][symbol]["quote"][convert]
    price = data["price"]
    timestamp = datetime.datetime.now()
    timestamps.append(timestamp)
    prices.append(price)
    # Update plot
    ax.plot(timestamps, prices, color="blue")
    ax.set_xlim(timestamps[0], timestamps[-1])
    ax.set_ylim(min(prices), max(prices))
    fig.canvas.draw()
    # Wait for time interval
    time.sleep(time_interval)

# Show plot
st.pyplot(fig)
