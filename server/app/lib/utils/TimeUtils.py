import time


def initTimer():
    return time.time()


def endTimer(initialTime: float, inMs=False) -> float:
    ms = time.time() - initialTime

    if inMs:
        return ms

    return ms / 1000
