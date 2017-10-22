import threading, time
import numpy as np
import cv2
import ctypes
from PIL import Image
from lib import Leap

import settings, utils

class CaptureLeapCamera(threading.Thread):
    controller = None
    frame_width = 640
    frame_height = 240
    sides = ['left', 'right']
    output = {}
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    path = {}
    out = None

    def image_to_pil(self, leap_image):
        address = int(leap_image.data_pointer)
        ctype_array_def = ctypes.c_ubyte * leap_image.width * leap_image.height
        # as ctypes array:
        as_ctype_array = ctype_array_def.from_address(address)
        # as numpy array:
        as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
        buffer = np.reshape(as_numpy_array, (leap_image.height, leap_image.width))
        # to PIL Image:
        pil_image = Image.fromarray(buffer, "L")
        # change format for QT:
        pil_image = pil_image.convert("RGB")

        return pil_image

    def convertCV(self,leap_img):
        pil_img = self.image_to_pil(leap_img)
        cv_img = np.array(pil_img)[:,:,::-1].copy()             #still has three channels
        return cv_img

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.process = None
        self.name = name

    def set_ready(self, is_ready):
        if not settings.is_ready['leap_camera']:
            with settings.lock:
                settings.is_ready['leap_camera'] = is_ready

    def preparing(self):
        while not utils.is_all_ready():
            frame = self.controller.frame()
            image = frame.images[0]

            if image.is_valid :
                self.set_ready(True)
            else:
                self.set_ready(False)

            if settings.exitFlag == True:
                self.stop()
                break
            time.sleep(0.300)

    def ready(self):
        raw_image = {}
        while(True):
            frame = self.controller.frame()
            image = frame.images[0]

            if image.is_valid:
                for i, s in enumerate(self.sides) :
                    # getting raw images
                    raw_image[s] = self.convertCV(frame.images[i])
                    # display images
                    cv2.imshow(s, raw_image[s])

                # write the flipped frame
                if settings.is_recording :
                    self.record(raw_image)
                elif self.output and self.output['left'] and self.output['left'].isOpened and self.output['left'].isOpened():
                    for i, s in enumerate(self.sides) :
                        self.output[s].release()

                if utils.wait_for_exit_key():
                    print 'Exit!'
                    break

            else:
                break

        self.stop()


    def record(self, raw_image):
        if not settings.is_open['leap_camera']:
            self.path = {
                'left': self.getPath('left'),
                'right': self.getPath('right')
            }
            for i, s in enumerate(self.sides) :
                self.output[s] = cv2.VideoWriter(self.path[s], self.fourcc, 40.0, (self.frame_width, self.frame_height))

            with settings.lock:
                settings.is_open['leap_camera'] = True

        if not self.output['left'].isOpened():
            # Define the codec and create VideoWriter object
            for i, s in enumerate(self.sides) :
                self.output[s].open(self.path[s] ,fourcc, 40.0, (self.frame_width, self.frame_height))


        for i, s in enumerate(self.sides) :
            self.output[s].write(raw_image[s])

    def getPath(self, key):
        return '/'.join(str(x) for x in [settings.path, settings.file_name, 'leap_' + key + '_' + str(settings.file_index)]) + '.avi'

    def run(self):
        self.controller = settings.leap_controller
        self.controller.set_policy_flags(Leap.Controller.POLICY_IMAGES)

        while(not settings.exitFlag):
            self.preparing()
            self.ready()
        self.stop()

    def stop(self):
        print "Trying to stop leap_camera "
        cv2.destroyAllWindows()
        for i, s in enumerate(self.sides) :
            self.output[s].release()

        # thread.exit()

        if self.process is not None:
            # Release everything if job is finished

            self.process.terminate()
            self.process = None
