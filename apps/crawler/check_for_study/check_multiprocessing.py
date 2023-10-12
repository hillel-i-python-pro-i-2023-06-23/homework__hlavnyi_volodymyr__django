# !!!
# for Study purpose only
# !!!

import multiprocessing
import time
import random


def worker(number):
    sleep = random.randint(1, 10)
    time.sleep(sleep)
    print(f"Multiprocessing: Worker {number} slept for {sleep} seconds")


for i in range(5):
    t = multiprocessing.Process(target=worker, args=(i,))
    t.start()
    print(f"Started worker {i}")
