import streamlit as st
import requests

# Set API endpoint and headers
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "c7271d78-54dd-4159-8409-6486b5f01e27"
}

# Set parameters for API request
params = {
    "start": "1",
    "limit": "10",
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
    coin_names = [coin["name"] for coin in data]
    coin_prices = [coin["quote"]["USD"]["price"] for coin in data]
    
    # Display data using Streamlit
    st.write("# Top 10 Cryptocurrencies by Market Cap")
    for i in range(len(coin_names)):
        st.write(f"{coin_names[i]}: {coin_prices[i]:,.2f} USD")
