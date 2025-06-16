import requests
import pandas as pd
from datetime import date
import datetime
import os

def fetch_btc_price_today():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {'ids': 'bitcoin', 'vs_currencies': 'usd'}
    response = requests.get(url, params=params)
    price = response.json()['bitcoin']['usd']
    today = datetime.date.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    new_data = pd.DataFrame([{"date": today, "price": price}])

    master_file = "data/historical/btc_prices.csv"


    if os.path.exists(master_file) and os.path.getsize(master_file) > 0:
        old = pd.read_csv(master_file)
        full = pd.concat([old, new_data], ignore_index=True).drop_duplicates(subset="date")
    else:
        full = new_data

    full.to_csv(master_file, index=False)

if __name__ == "__main__":
    fetch_btc_price_today()
