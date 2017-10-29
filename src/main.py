import os, cv2, time

import settings

from CaptureFacetimeCamera import CaptureFacetimeCamera
from CaptureLeapCamera import CaptureLeapCamera
from CaptureLeapApi import CaptureLeapApi
import json

def set_file_name (value) :
    with settings.lock:
        settings.file_name = value

def set_file_index (value) :
    with settings.lock:
        settings.file_index = value

def set_is_recording (value) :
    with settings.lock:
        settings.is_recording = value

def set_settings (key, value) :
    {
        'file_name': set_file_name,
        'file_index': set_file_index,
        'is_recording': set_is_recording
    }[key](value)

def set_settings_in_helper (arr_key, value, obj) :
    if len(arr_key) == 1 :
        with settings.lock:
            obj[arr_key[0]] = value
    else :
        key = arr_key.pop()
        set_settings_in (arr_key, value, obj[key])

def set_settings_in (arr_key, value) :
    set_settings_in_helper(arr_key, value, settings)

def is_all_finish () :
    return not any(value for key, value in settings.is_open.iteritems())

def is_all_ready () :
    return all(value for key, value in settings.is_ready.iteritems())

def wait_for_finish () :
    while any(value for key, value in settings.is_open.iteritems()) :
        time.sleep(0.100)

def wait_for_exit_key():
    if (cv2.waitKey(1) & 0xFF == ord('q')) | settings.exitFlag == True :
        with settings.lock:
            settings.exitFlag = True
        return True
    else:
        return False

def exit () :
    with settings.lock:
        settings.exitFlag = True

def start_record () :
    # with settings.lock:
    #     for key in settings.is_open:
    #         settings.is_open[key] = False

    set_settings('is_recording', True)

def stop_record () :
    set_settings('is_recording', False)

def init () :
    captureFacetimeCamera = CaptureFacetimeCamera(name = "CaptureFacetimeCamera")
    captureFacetimeCamera.start()

    captureLeapCamera = CaptureLeapCamera(name = "CaptureLeapCamera")
    captureLeapCamera.start()

    captureLeapApi = CaptureLeapApi(name = "CaptureLeapApi")
    captureLeapApi.start()

    # captureFacetimeCamera.join()
