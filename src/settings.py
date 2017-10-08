import threading

from lib import Leap

def init():
    global lock
    lock = threading.Lock()

    global exitFlag
    exitFlag = False

    global leap_controller
    leap_controller = Leap.Controller()
