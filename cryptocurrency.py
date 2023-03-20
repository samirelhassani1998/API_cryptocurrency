import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set API endpoint and headers
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "c7271d78-54dd-4159-8409-6486b5f01e27"
}

# Set parameters for API request
params = {
    "start": "1",
    "limit": "100", # Increase limit to get more data
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
    coin_df = pd.DataFrame(data) # Convert data to pandas DataFrame
    coin_df = coin_df[['name', 'symbol', 'cmc_rank', 'date_added', 'total_supply', 'quote']]
    coin_df = coin_df[coin_df['cmc_rank'] <= 100] # Filter out low ranked coins
    coin_df['date_added'] = pd.to_datetime(coin_df['date_added']) # Convert date to datetime format
    coin_df['market_cap'] = coin_df['quote'].apply(lambda x: x['USD']['market_cap']) # Extract market cap data
    
    # Time-series analysis of cryptocurrency prices over different time intervals (e.g., hourly, daily, weekly, monthly).
    st.write("# Time-series Analysis of Cryptocurrency Prices")
    time_interval = st.selectbox("Select Time Interval", ["Hourly", "Daily", "Weekly", "Monthly"])
    if time_interval == "Hourly":
        freq = "H"
    elif time_interval == "Daily":
        freq = "D"
    elif time_interval == "Weekly":
        freq = "W"
    else:
        freq = "M"
    coin_df.set_index('date_added', inplace=True)
    grouped_df = coin_df.groupby('symbol')['market_cap'].resample(freq).mean().unstack()
    st.line_chart(grouped_df)
    
    # Correlation analysis between different cryptocurrencies and/or their prices.
    st.write("# Correlation Analysis of Cryptocurrency Prices")
    corr_df = coin_df.pivot_table(index='date_added', columns='symbol', values='market_cap')
    corr = corr_df.corr()
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
    market_cap = coin_df.groupby('date_added')['market_cap'].sum()
    st.line_chart(market_cap)
   
