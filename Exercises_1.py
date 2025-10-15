import threading
from random import randint
import time


def print_thread_name():
    sleep_time = randint(1, 5)
    time.sleep(sleep_time)

    print(f"[Thread]: {threading.current_thread().name}, sleep time: {sleep_time} sec")


threads = []
quantity = int(input("Please, enter quantity of threads: "))

for i in range(quantity):
    thread = threading.Thread(target=print_thread_name)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
