from lib import Leap

from CaptureFacetimeCamera import CaptureFacetimeCamera
from CaptureLeapCamera import CaptureLeapCamera
import CaptureLeapApi, json

import settings

if __name__ == '__main__':
    settings.init()

    captureFacetimeCamera = CaptureFacetimeCamera(name = "CaptureFacetimeCamera")
    captureFacetimeCamera.start()

    captureLeapCamera = CaptureLeapCamera(name = "CaptureLeapCamera")
    captureLeapCamera.start()

    CaptureLeapApi.main()
    
    while(True):
        record = raw_input("Record")
        if record == "y":
            settings.is_recording = True
        else:
            settings.is_recording = False
