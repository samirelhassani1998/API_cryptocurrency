import streamlit as st
import requests

# Set up the API endpoint and headers
api_endpoint = "https://rest.coinapi.io/v1/exchangerate/{}/{}"
headers = {"X-CoinAPI-Key": "Y6A1A2057-BABF-49F7-A562-FCF109B6BD2E"}

# Define the cryptocurrencies and fiat currencies to retrieve prices for
cryptocurrencies = ["BTC", "ETH", "XRP"]
fiat_currencies = ["USD", "EUR", "GBP"]

# Create a list to store the retrieved prices
prices = []

# Loop through each cryptocurrency and fiat currency combination, retrieve the price,
# and add it to the list of prices
for crypto in cryptocurrencies:
    for fiat in fiat_currencies:
        url = api_endpoint.format(crypto, fiat)
        response = requests.get(url, headers=headers)
        data = response.json()
        print("Code d'état de la réponse :", response.status_code)
        print("Texte de la réponse :", response.text)
        print("Données JSON :", data)
        prices.append((crypto, fiat, data["rate"]))

# Create a Streamlit app to display the prices
st.title("Cryptocurrency Prices")

# Create a table to display the prices
table_header = ["Cryptocurrency", "Fiat Currency", "Price"]
table_data = [[crypto, fiat, price] for crypto, fiat, price in prices]
st.table(table_data, header=table_header)
