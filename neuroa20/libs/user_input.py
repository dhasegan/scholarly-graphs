import time
import random

def _sleep():
    wait_time = random.randint(1, 10)
    print('waiting...', wait_time)
    time.sleep(wait_time)

def _get_in(text, opts):
    while True:
        val = input(text)
        if val in opts:
            break
    return val