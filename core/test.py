import numpy as np
usd = list()
for i in range(20):
    usd.append(i)
    if len(usd) > 10:
        usd.pop(0)

print(usd)
arr_mean = np.mean(usd)
arr_var = np.var(usd)
arr_std = np.std(usd)

print("平均值为：%f" % arr_mean)
print("方差为：%f" % arr_var)
print("标准差为:%f" % arr_std)
