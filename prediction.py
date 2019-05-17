import readData_US
import matplotlib.pyplot as plt

show_plot = True


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

    return data


def main():
    data = readData_US.get_stock_prices_us('GOOG')
    data = pre_process(data)
    print(data[:100])


if __name__ == '__main__':
    main()
