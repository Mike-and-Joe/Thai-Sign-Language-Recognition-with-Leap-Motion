import threading

from lib import Leap

def init():
    global path
    path = 'record'

    global lock
    lock = threading.Lock()

    global leap_controller
    leap_controller = Leap.Controller()

    global exitFlag
    exitFlag = False

    global is_ready
    is_ready = {'facetime': False, 'leap': False}

    global is_recording
    is_recording = True

    global file_name
    file_name = ''

    global file_index
    file_index = 0
