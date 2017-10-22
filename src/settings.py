import threading

from lib import Leap

def init():
    global path
    path = 'record'

    global camera_index
    camera_index = 1

    global lock
    lock = threading.Lock()

    global leap_controller
    leap_controller = Leap.Controller()

    global exitFlag
    exitFlag = False

    global is_ready
    is_ready = {'facetime': False, 'leap_camera': False, 'leap_api': False}

    global is_recording
    is_recording = False

    global is_open
    is_open = {'facetime': False, 'leap_camera': False, 'leap_api': False}

    global file_name
    file_name = ''

    global file_index
    file_index = 0
