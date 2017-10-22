import os

import settings

from CaptureFacetimeCamera import CaptureFacetimeCamera
from CaptureLeapCamera import CaptureLeapCamera
from CaptureLeapApi import CaptureLeapApi
import json

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

def start_record () :
    with settings.lock:
        for key in settings.is_open:
            settings.is_open[key] = False

        settings.is_recording = True

def stop_record () :
    set_is_recording(False)

def init () :
    captureFacetimeCamera = CaptureFacetimeCamera(name = "CaptureFacetimeCamera")
    captureFacetimeCamera.start()

    captureLeapCamera = CaptureLeapCamera(name = "CaptureLeapCamera")
    captureLeapCamera.start()

    # captureLeapApi = CaptureLeapApi(name = "CaptureLeapApi")
    # captureLeapApi.start()

    # captureFacetimeCamera.join()
