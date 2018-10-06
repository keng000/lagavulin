from contextlib import contextmanager
from datetime import datetime


def time_measure_decorator(func):
    def wrapper(*args, **kwargs):
        st = datetime.now()
        ret = func(*args, **kwargs)
        print(f"Time Spent: {(datetime.now() - st).total_seconds():.3f}s")
        return ret

    return wrapper

"""time_measure_decorator sample
@time_measure_decorator
def func():
    # some processing
    pass

"""

@contextmanager
def time_measure_manager(msg=None):
    if msg is not None:
        print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg} Start.')
    st = datetime.now()

    yield

    if msg is not None:
        print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg} End. ', end="")
    print(f"Time Spent: {(datetime.now() - st).total_seconds():.3f}s")


""" time_measure_manager(contextmanager) sample
import time
for idx in range(5):
    with time_measure_manager():
        time.sleep(0.5)
"""
