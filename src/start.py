from lib import Leap

from CaptureFacetimeCamera import CaptureFacetimeCamera
from CaptureLeapCamera import CaptureLeapCamera
from CaptureLeapApi import SampleListener

import settings

if __name__ == '__main__':
    settings.init()

    captureFacetimeCamera = CaptureFacetimeCamera(name = "CaptureFacetimeCamera")
    captureFacetimeCamera.start()

    # captureLeapCamera = CaptureLeapCamera(name = "CaptureLeapCamera")
    # captureLeapCamera.start()