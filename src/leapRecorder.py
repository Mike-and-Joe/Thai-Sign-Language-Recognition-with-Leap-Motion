from CaptureLeapCamera import CaptureLeapCamera
from CaptureFacetimeCamera import CaptureFacetimeCamera

if __name__ == '__main__':
    captureFacetimeCamera = CaptureFacetimeCamera(name = "CaptureFacetimeCamera")
    captureFacetimeCamera.start()

    captureLeapCamera = CaptureLeapCamera(name = "CaptureLeapCamera")
    captureLeapCamera.start()
