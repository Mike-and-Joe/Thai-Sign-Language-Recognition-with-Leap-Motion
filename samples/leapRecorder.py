from Capture import CaptureLeapCamera
from Capture import CaptureFacetimeCamera
    
if __name__ == '__main__':
    captureFacetimeCamera = CaptureFacetimeCamera(name = "CaptureFacetimeCamera")
    captureFacetimeCamera.start()

    captureLeapCamera = CaptureLeapCamera()
    captureLeapCamera.main()