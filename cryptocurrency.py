import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set API endpoint and headers
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical"
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "c7271d78-54dd-4159-8409-6486b5f01e27"
}

# Set parameters for API request
params = {
    "symbol": "BTC",
    "time_start": "2022-01-01T00:00:00Z",
    "time_end": "2022-12-31T23:59:59Z",
    "interval": "daily",
    "convert": "USD"
}

# Make API request
response = requests.get(url, headers=headers, params=params)

# Check if API request is successful
if response.status_code != 200:
    st.error("Failed to retrieve data from CoinMarketCap API - check your API Key and try again.")
else:
    # Parse API response and extract relevant data
    data = response.json()["data"]
    coin_df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "market_cap"]) # Convert data to pandas DataFrame
    coin_df['timestamp'] = pd.to_datetime(coin_df['timestamp'], format="%Y-%m-%dT%H:%M:%S.%fZ") # Convert timestamp to datetime format
    coin_df.set_index('timestamp', inplace=True) # Set timestamp as index
    coin_df = coin_df[['open', 'high', 'low', 'close', 'volume', 'market_cap']] # Select relevant columns

    # Time-series analysis of cryptocurrency prices over different time intervals (e.g., hourly, daily, weekly, monthly).
    st.write("# Time-series Analysis of BTC Prices in 2022")
    time_interval = st.selectbox("Select Time Interval", ["Hourly", "Daily", "Weekly", "Monthly"])
    if time_interval == "Hourly":
        freq = "H"
    elif time_interval == "Daily":
        freq = "D"
    elif time_interval == "Weekly":
        freq = "W"
    else:
        freq = "M"
    grouped_df = coin_df.resample(freq).mean()
    st.line_chart(grouped_df['close'])
    
    # Correlation analysis between different cryptocurrencies and/or their prices.
    st.write("# Correlation Analysis of Cryptocurrency Prices")
    corr = coin_df.corr()
    fig, ax = plt.subplots()
    cax = ax.imshow(corr, cmap='coolwarm')
    ax.set_xticks(np.arange(len(corr.columns)))
    ax.set_yticks(np.arange(len(corr.columns)))
    ax.set_xticklabels(corr.columns)
    ax.set_yticklabels(corr.columns)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    fig.colorbar(cax)
    st.pyplot(fig)
    
    # Visualization of cryptocurrency market capitalization over time.
    st.write("# Market Capitalization Over Time")
    market_cap = coin_df['market_cap']
    st.line_chart(market_cap)
