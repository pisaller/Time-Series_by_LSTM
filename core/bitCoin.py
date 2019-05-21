import smtplib
from email.mime.text import MIMEText
import numpy as np
from datetime import datetime, timedelta
import time

import requests


def send_mail(receiver_addresses, content, change_rate,  arr_mean, arr_var, arr_std):

    # Please check the following website to set your own email config
    # https://www.runoob.com/python/python-email.html

    host = 'smtp.163.com'  # Your own email host
    port = 25
    sender = 'andy1994416@163.com'  # Your own email
    pwd = '*********'  # Your own password
    body = '<h2>温馨提醒：</h2>' \
           '<h3> 当前美元价格： {}</h3>' \
           '<h3> 折合人民币价格(汇率=7)： {} </h3>' \
           '<p> 2小时内变化率： {} </p>' \
           '<p> 2小时内平均值： {} </p>' \
           '<p> 2小时内反差： {} </p>' \
           '<p> 2小时内标准差： {} </p>'.format(content, content * 7, change_rate,  arr_mean, arr_var, arr_std)

    msg = MIMEText(body, 'html', "utf-8")
    msg['Subject'] = '比特币波动提醒！'
    msg['From'] = sender

    # Sometimes STMP server might block your request for no reason.
    # The solution is to include the sender's email address to the receivers' list.

    msg['To'] = '{}, andy1994416@163.com'.format(receiver_addresses)   # Add sender's email
    s = smtplib.SMTP(host, port)
    s.login(sender, pwd)
    s.sendmail(msg["From"], msg["To"].split(","), msg.as_string())


def get_bitcoin():
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"

    headers = {
        'User-Agent': "PostmanRuntime/7.13.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "8d7657ec-1f45-41ab-a214-39429044ba46,c24ace01-c2b5-4dc4-80b4-b6109b8f8e15",
        'Host': "api.coindesk.com",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)
    bitcoin_usd = round(response.json()['bpi']['USD']['rate_float'], 3)

    return bitcoin_usd


def monitoring(bitcoin_usd, freq):
    history_list.append(bitcoin_usd)
    if len(history_list) > freq:
        history_list.pop(0)

    arr_mean = round(float(np.mean(history_list)), 3)
    arr_var = round(float(np.var(history_list)), 3)
    arr_std = round(float(np.std(history_list)), 3)

    min_value = min(history_list)
    max_value = max(history_list)

    change_rate = round(100 * (max_value - min_value) / arr_mean, 2)

    return arr_mean, arr_var, arr_std, change_rate


def main():

    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # receivers = 'bai_haochen@163.com'
    receivers = '281815376@qq.com'
    frequency = 120

    bitcoin_usd = get_bitcoin()

    arr_mean, arr_var, arr_std, change_rate = monitoring(bitcoin_usd, frequency)
    print('BitCoin: \t {} \t Current Price: ${} \t Change Rate: {}% \t 2HR Average: ${}'.format(today, bitcoin_usd,
                                                                                                change_rate, arr_mean))
    if change_rate > 5:
        send_mail(receivers, bitcoin_usd, arr_mean, arr_var, arr_std, change_rate)


if __name__ == '__main__':
    history_list = list()
    while True:

        dt = datetime.now() + timedelta(minutes=1)
        dt = dt.replace(second=0)

        try:
            main()
        except Exception as e:
            print(e)

        while datetime.now() < dt:
            time.sleep(1)
