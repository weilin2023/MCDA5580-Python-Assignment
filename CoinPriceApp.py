import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt


def get_all_coins():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    data = response.json()
    print(data)
    return {coin['id']: coin['name'] for coin in data}


def fetch_coin_data(coin_id, days):
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-Vm3PdgttBcF8Z7CQGVPLreFt",

    }
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def plot_data(coin_data):
    df = pd.DataFrame(coin_data['prices'], columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)

    volume_df = pd.DataFrame(coin_data['total_volumes'], columns=['timestamp', 'volume'])
    volume_df['date'] = pd.to_datetime(volume_df['timestamp'], unit='ms')
    volume_df.set_index('date', inplace=True)

    max_volume = volume_df['volume'].max()
    min_volume = volume_df['volume'].min()
    max_volume_date = volume_df[volume_df['volume'] == max_volume].index[0]
    min_volume_date = volume_df[volume_df['volume'] == min_volume].index[0]

    # Find max and min
    max_price = df['price'].max()
    min_price = df['price'].min()
    max_date = df[df['price'] == max_price].index[0]
    min_date = df[df['price'] == min_price].index[0]

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['price'], label='Price')
    plt.scatter([max_date, min_date], [max_price, min_price], color='red')  # mark the max and min
    plt.title(f'Price of {coin_id} over the last {days} days')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    return max_price, min_price, max_date, min_date, max_volume, min_volume, max_volume_date, min_volume_date


if __name__ == '__main__':
    # Streamlit UI
    st.title('Cryptocurrency Price Analysis App')
    coins = get_all_coins()
    days = '365'  # Set to '365' for the last year
    coin_id = st.selectbox('Select the first cryptocurrency:', list(coins.keys()), format_func=lambda x: coins[x])

    if st.button('Fetch Data'):

        if coin_id.lower() in coins:
            prices = fetch_coin_data(coin_id, days)
            max_price, min_price, max_date, min_date, max_volume, min_volume, max_volume_date, min_volume_date\
                = plot_data(prices)
            st.write(f"The maximum price was ${max_price:.2f} on {max_date.strftime('%Y-%m-%d')}.")
            st.write(f"The minimum price was ${min_price:.2f} on {min_date.strftime('%Y-%m-%d')}.")
            st.write(f"The maximum volume was {max_volume:.2f} on {max_volume_date.strftime('%Y-%m-%d')}.")
            st.write(f"The minimum volume was {min_volume:.2f} on {min_volume_date.strftime('%Y-%m-%d')}.")
        else:
            st.write("Invalid Cryptocurrency Name")
