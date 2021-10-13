import random


def incremental_backoff(minimum=0.3, maximum=30, increase=1.5):
    """ Incremental backoff between connection attempts """
    wait_time = minimum  # time is in seconds
    while True:
        yield wait_time
        wait_time = min(wait_time * increase, maximum)
        wait_time *= (100 + random.randint(0, 50)) / 100
