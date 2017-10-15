import os

import settings

from CaptureFacetimeCamera import CaptureFacetimeCamera
from CaptureLeapCamera import CaptureLeapCamera
import CaptureLeapApi, json

def create_folder(directory) :
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_last_index_from_folder(directory) :
    arr_txt = [x for x in os.listdir(directory) if x.endswith(".txt")]
    if len(arr_txt):
        return int(arr_txt[len(arr_txt)-1].split('.')[0])
    else:
        return 0

def set_file_name (file_name) :
    with settings.lock:
        settings.file_name = file_name

def set_file_index (file_index) :
    with settings.lock:
        settings.file_index = file_index

def set_is_recording (is_recording) :
    with settings.lock:
        settings.is_recording = is_recording

def exit () :
    with settings.lock:
        settings.exitFlag = True

def init () :
    captureFacetimeCamera = CaptureFacetimeCamera(name = "CaptureFacetimeCamera")
    captureFacetimeCamera.start()

    captureLeapCamera = CaptureLeapCamera(name = "CaptureLeapCamera")
    captureLeapCamera.start()
