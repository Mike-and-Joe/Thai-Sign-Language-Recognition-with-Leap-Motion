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
    def leap_to_array(self,leap_img):
        imdata = ctypes.cast(leap_img.data.cast().__long__(), ctypes.POINTER(leap_img.width*leap_img.height*ctypes.c_ubyte)).contents
        return np.reshape(np.array(imdata,'int'),(leap_img.height,leap_img.width))

    def convertPIL(self,leap_img):
        return Image.fromarray(self.leap_to_array(leap_img)).convert("RGB")

    def convertCV(self,leap_img):
        pil_img = self.convertPIL(leap_img)
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
        out_left = cv2.VideoWriter('./record/leap_camera/left.avi',fourcc, 20.0, (frame_width,frame_height))
        out_right = cv2.VideoWriter('./record/leap_camera/right.avi',fourcc, 20.0, (frame_width,frame_height))

        while(True):
            frame = controller.frame()
            image = frame.images[0]

            if image.is_valid & ((not settings.is_ready['facetime']) | (not settings.is_ready['leap'])):
                self.wait_for_ready()
            elif image.is_valid:

                undistorted_left = self.convertCV(frame.images[0])
                undistorted_right = self.convertCV(frame.images[1])

                # convert frame to rgb
                # undistorted_left = cv2.cvtColor(undistorted_left, cv2.COLOR_GRAY2RGB)
                # undistorted_right = cv2.cvtColor(undistorted_right, cv2.COLOR_GRAY2RGB)

                # display images
                cv2.imshow('Left Camera', undistorted_left)
                cv2.imshow('Right Camera', undistorted_right)

                # save video
                if settings.is_recording:
                    cv2.waitKey(1)

                    if not out_left.isOpened():
                        # Define the codec and create VideoWriter object
                        out_left.open('./record/leap_camera/left.avi',fourcc, 20.0, (frame_width,frame_height))
                        out_right.open('./record/leap_camera/right.avi',fourcc, 20.0, (frame_width,frame_height))

                    out_left.write(undistorted_left)
                    out_right.write(undistorted_right)
                elif out_left.isOpened():
                    out_left.release()
                    out_right.release()
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
