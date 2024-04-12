import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt


# Function to get all available coins
def get_all_coins():
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-Vm3PdgttBcF8Z7CQGVPLreFt",

    }
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url, headers=headers)
    data = response.json()
    return {coin['id']: coin['name'] for coin in data}


# Function to fetch coin data from CoinGecko API
def fetch_coin_data(coin_id, days):
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-Vm3PdgttBcF8Z7CQGVPLreFt",

    }
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['prices']


# Function to plot data for two coins
def plot_data(prices1, prices2, coin1, coin2, days):
    df1 = pd.DataFrame(prices1, columns=['timestamp', 'price'])
    df1['date'] = pd.to_datetime(df1['timestamp'], unit='ms')
    df1.set_index('date', inplace=True)

    df2 = pd.DataFrame(prices2, columns=['timestamp', 'price'])
    df2['date'] = pd.to_datetime(df2['timestamp'], unit='ms')
    df2.set_index('date', inplace=True)

    plt.figure(figsize=(10, 5))
    plt.plot(df1.index, df1['price'], label=f'{coin1} Price')
    plt.plot(df2.index, df2['price'], label=f'{coin2} Price')
    plt.title(f'Price Comparison of {coin1} vs {coin2} over {days}')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)


if __name__ == '__main__':
    # Streamlit UI setup
    st.title('Cryptocurrency Price Comparison App')

    # Loading coin data
    coins = get_all_coins()
    coin1 = st.selectbox('Select the first cryptocurrency:', list(coins.keys()), format_func=lambda x: coins[x])
    coin2 = st.selectbox('Select the second cryptocurrency:', list(coins.keys()), format_func=lambda x: coins[x])

    # Time frame options
    time_frames = {'1 week': 7, '1 month': 30, '3 months': 90, '1 year': 365}
    selected_time_frame = st.selectbox('Select the time frame:', list(time_frames.keys()))

    if st.button('Compare Prices'):
        days = time_frames[selected_time_frame]
        prices1 = fetch_coin_data(coin1, days)
        prices2 = fetch_coin_data(coin2, days)
        plot_data(prices1, prices2, coin1, coin2, selected_time_frame)
