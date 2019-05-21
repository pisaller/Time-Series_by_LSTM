import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

import readData_US

show_plot = False


def pre_process(data):
    data = data.sort_values('Date').reset_index(drop=True)

    if show_plot is True:
        freq = 60
        plt.figure(figsize=(21, 9))
        plt.title('Time Series', fontsize=18)
        plt.plot(range(data.shape[0]), data['High'])
        plt.xticks(range(0, data.shape[0], freq), data['Date'].loc[::freq], rotation=45)
        plt.xlabel('Date (Every {} days)'.format(freq), fontsize=14)
        plt.ylabel('Highest Price', fontsize=14)
        plt.show()

    # Highest price is our target value of prediction
    highest_price = data.High.values
    print('Sample Size: ', len(highest_price))
    # Split the data by 8/2
    train_data_length = int(len(highest_price) * 0.8)
    train_data = highest_price[:train_data_length]
    test_data = highest_price[train_data_length:]

    scaler = MinMaxScaler()
    train_data = train_data.reshape(-1, 1)
    test_data = test_data.reshape(-1, 1)

    # todo: reverse the order to descending, keep the most recent period clean.
    smoothing_window_size = 360
    di = int
    for di in range(0, train_data_length, smoothing_window_size):
        if di + smoothing_window_size <= train_data_length:
            scaler.fit(train_data[di:di + smoothing_window_size, :])
            train_data[di:di + smoothing_window_size, :] = scaler.transform(
                train_data[di:di + smoothing_window_size, :])

    # Normalize the last bit of remaining data
    scaler.fit(train_data[di:, :])
    train_data[di:, :] = scaler.transform(train_data[di:, :])
    train_data = train_data.reshape(-1)
    test_data = scaler.transform(test_data).reshape(-1)

    return train_data, test_data


def main():
    data = readData_US.get_stock_prices_us('AAL')
    data = pre_process(data)
    print(data[:100])


if __name__ == '__main__':
    main()
