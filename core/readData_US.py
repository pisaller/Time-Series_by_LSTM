import datetime as dt
import json
import os
import urllib.request

import pandas as pd

# Please get your own FREE api key on https://www.alphavantage.co/support/#api-key
api_key = '8H5AO0K6RF3VZPLT'


def mkdir(path):
    path = path.strip()
    exist = os.path.exists(path)
    if not exist:
        os.makedirs(path)
        print('Folder: "{}" Successfully Built'.format(path))
        return True
    else:
        print('Folder: "{}" Already Exist'.format(path))
        return False


def get_stock_prices_us(ticker):
    ticker = ticker.upper()
    url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s" % (
        ticker, api_key)

    # Create a folder to save the downloaded data
    mkpath = "data"
    mkdir(mkpath)
    # Save data to this directory
    file_to_save = 'data/us_market-{}.csv'.format(ticker)

    # To check if that ticker is already downloaded to local
    if not os.path.exists(file_to_save):
        print('Downloading Data of {}...'.format(ticker))
        with urllib.request.urlopen(url_string) as url:
            data = json.loads(url.read().decode())
            data = data['Time Series (Daily)']
            df = pd.DataFrame(columns=['Date', 'Low', 'High', 'Close', 'Open'])
            for k, v in data.items():
                date = dt.datetime.strptime(k, '%Y-%m-%d')
                data_row = [date.date(), float(v['3. low']), float(v['2. high']),
                            float(v['4. close']), float(v['1. open'])]
                df.loc[-1, :] = data_row
                df.index = df.index + 1
        print('Data saved to : %s' % file_to_save)
        df.to_csv(file_to_save, index=False)

    else:
        print('File already exists. Loading data from local...')
        df = pd.read_csv(file_to_save)

    return df


if __name__ == '__main__':
    get_stock_prices_us('AAL')
