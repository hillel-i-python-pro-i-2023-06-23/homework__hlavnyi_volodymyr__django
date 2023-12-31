# !!!
# for Study purpose only
# !!!

import threading
import time
import random


def worker(number):
    sleep = random.randint(1, 5)
    time.sleep(sleep)
    print(f"Threads: Worker {number} slept for {sleep} seconds")


for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    print(f"Started worker {i}")
