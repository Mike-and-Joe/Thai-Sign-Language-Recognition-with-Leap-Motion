# -*- coding: utf-8 -*-
"""
Created on Sun Oct 08 12:21:05 2017

@author: Pakpoom
"""

import threading
import numpy as np
import cv2
import ctypes
from PIL import Image
from lib import Leap

import settings

class CaptureLeapCamera(threading.Thread):
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

    def checkImageAllow(controller):
        imagesAllowed = controller.config.get("tracking_images_mode") == 2
        if not imagesAllowed:
            # ask user for permission...
            controller.config.set("tracking_images_mode", 2)
            controller.config.save()

    def wait_for_ready(self):
        while(True):
            if not settings.is_ready['leap']:
                with settings.lock:
                    settings.is_ready['leap'] = True
            elif settings.is_ready['facetime']:
                break

    def capture(self):
        controller = settings.leap_controller
        controller.set_policy_flags(Leap.Controller.POLICY_IMAGES)

        frame_width = 640
        frame_height = 240

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        sides = ['left', 'right']
        raw_image = {}
        output = {}

        for i, s in enumerate(sides) :
            output[s] = cv2.VideoWriter('./record/leap_camera/' + str(s) + '.avi',fourcc, 40.0, (frame_width,frame_height))

        while(True):
            frame = controller.frame()
            image = frame.images[0]

            if image.is_valid & ((not settings.is_ready['facetime']) | (not settings.is_ready['leap'])):
                self.wait_for_ready()
            elif image.is_valid:
                for i, s in enumerate(sides) :
                    # getting raw images
                    raw_image[s] = self.convertCV(frame.images[i])
                    # display images
                    cv2.imshow(s, raw_image[s])

                # save video
                if settings.is_recording:
                    cv2.waitKey(1)

                    if not output['left'].isOpened():
                        # Define the codec and create VideoWriter object
                        for i, s in enumerate(sides) :
                            output[s].open('./record/leap_camera/' + str(s) + '.avi',fourcc, 40.0, (frame_width,frame_height))

                    for i, s in enumerate(sides) :
                        output[s].write(raw_image[s])

                elif output['left'].isOpened():
                    for i, s in enumerate(sides) :
                        output[s].release()

                elif (cv2.waitKey(1) & 0xFF == ord('q')) | settings.exitFlag == True :
                    with settings.lock:
                        settings.exitFlag = True
                    break

        cv2.destroyAllWindows()

    def run(self):
        try:
            self.capture()
        except KeyboardInterrupt:
            sys.exit(0)
