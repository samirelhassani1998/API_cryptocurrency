import streamlit as st
import requests
import pandas as pd
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt

# Set API endpoint and headers
url = "https://api.binance.com/api/v3/ticker/price"
symbol = "BTCUSDT"

# Time interval in seconds
time_interval = 5

# Set up empty lists for timestamp and price data
timestamps = []
prices = []

# Set up plot
fig, ax = plt.subplots()
ax.set_title("BTC/USDT Price")

# Main program loop
while True:
    # Make API request
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error("Failed to retrieve data from Binance API - check your API Key and try again.")
        break
    data = response.json()
    price = float(data["price"])
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
