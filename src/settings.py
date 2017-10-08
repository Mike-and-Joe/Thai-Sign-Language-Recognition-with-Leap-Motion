import threading

def init():
    global lock
    lock = threading.Lock()

    global exitFlag
    exitFlag = False
