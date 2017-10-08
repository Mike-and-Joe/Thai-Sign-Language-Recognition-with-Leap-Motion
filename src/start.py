import threading

from CaptureLeapCamera import CaptureLeapCamera
from CaptureFacetimeCamera import CaptureFacetimeCamera
from CaptureLeapApi import SampleListener
from lib import Leap

exitFlag = threading.Condition()

if __name__ == '__main__':
    captureFacetimeCamera = CaptureFacetimeCamera(name = "CaptureFacetimeCamera")
    captureFacetimeCamera.start()

    # captureLeapCamera = CaptureLeapCamera(name = "CaptureLeapCamera")
    # captureLeapCamera.start()