from multiprocessing import Pool
from datetime import datetime


def f(x):
    return x**x


data = list(range(1, 7000))
# print(data)
t11 = datetime.now()
print("Satrt time: ", t11.strftime("%H:%M:%S"))
data_out = [i**i for i in data]
# print(data_out)
t12 = datetime.now()
print("End time: ", t12.strftime("%H:%M:%S"))
r1 = t12 - t11
print("Time delta: ", r1)

print("============")

t21 = datetime.now()
print("Satrt time: ", t21.strftime("%H:%M:%S"))
with Pool(20) as p:
    # p = Pool(3)
    # print(p.map(f, list(data)))
    p.map(f, list(data))

t22 = datetime.now()
print("End time: ", t22.strftime("%H:%M:%S"))
print("Time delta: ", t22 - t21)
print("============")
r2 = t22 - t21
print("Delta: ", r1 - r2)
