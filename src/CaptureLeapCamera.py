# -*- coding: utf-8 -*-
"""
Created on Sun Oct 08 12:21:05 2017

@author: Pakpoom
"""

import threading
import cv2
import numpy as np
import ctypes
from lib import Leap

import settings

class CaptureLeapCamera(threading.Thread):
    def undistort(self, image, coordinate_map, coefficient_map, width, height):
        destination = np.empty((width, height), dtype = np.ubyte)

        #wrap image data in numpy array
        i_address = int(image.data_pointer)
        ctype_array_def = ctypes.c_ubyte * image.height * image.width
        # as ctypes array
        as_ctype_array = ctype_array_def.from_address(i_address)
        # as numpy array
        as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
        img = np.reshape(as_numpy_array, (image.height, image.width))

        #remap image to destination
        destination = cv2.remap(img,
                                coordinate_map,
                                coefficient_map,
                                interpolation = cv2.INTER_LINEAR)

        #resize output to desired destination size
        destination = cv2.resize(destination,
                                (width, height),
                                0, 0,
                                cv2.INTER_LINEAR)
        return destination

    def convert_distortion_maps(self, image):

        distortion_length = image.distortion_width * image.distortion_height
        xmap = np.zeros(distortion_length/2, dtype=np.float32)
        ymap = np.zeros(distortion_length/2, dtype=np.float32)

        for i in range(0, distortion_length, 2):
            xmap[distortion_length/2 - i/2 - 1] = image.distortion[i] * image.width
            ymap[distortion_length/2 - i/2 - 1] = image.distortion[i + 1] * image.height

        xmap = np.reshape(xmap, (image.distortion_height, image.distortion_width/2))
        ymap = np.reshape(ymap, (image.distortion_height, image.distortion_width/2))

        #resize the distortion map to equal desired destination image size
        resized_xmap = cv2.resize(xmap,
                                (image.width, image.height),
                                0, 0,
                                cv2.INTER_LINEAR)
        resized_ymap = cv2.resize(ymap,
                                (image.width, image.height),
                                0, 0,
                                cv2.INTER_LINEAR)

        #Use faster fixed point maps
        coordinate_map, interpolation_coefficients = cv2.convertMaps(resized_xmap,
                                                                    resized_ymap,
                                                                    cv2.CV_32FC1,
                                                                    nninterpolation = False)

        return coordinate_map, interpolation_coefficients

    def checkImageAllow(controller):
        imagesAllowed = controller.config.get("tracking_images_mode") == 2
        if not imagesAllowed:
            # ask user for permission...
            controller.config.set("tracking_images_mode", 2)
            controller.config.save()

    def capture(self):
        controller = settings.leap_controller
        controller.set_policy_flags(Leap.Controller.POLICY_IMAGES)

        maps_initialized = False

        frame_width = 400
        frame_height = 400

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out_left = cv2.VideoWriter('./record/leap_camera/left.avi',fourcc, 20.0, (frame_width,frame_height))
        out_right = cv2.VideoWriter('./record/leap_camera/right.avi',fourcc, 20.0, (frame_width,frame_height))

        while(True):
            frame = controller.frame()
            image = frame.images[0]
            if image.is_valid:
                if not maps_initialized:
                    left_coordinates, left_coefficients = self.convert_distortion_maps(frame.images[0])
                    right_coordinates, right_coefficients = self.convert_distortion_maps(frame.images[1])
                    maps_initialized = True

                undistorted_left = self.undistort(image, left_coordinates, left_coefficients, frame_width, frame_height)
                undistorted_right = self.undistort(image, right_coordinates, right_coefficients, frame_width, frame_height)

                #convert frame to rgb 
                undistorted_left = cv2.cvtColor(undistorted_left, cv2.COLOR_GRAY2RGB)
                undistorted_right = cv2.cvtColor(undistorted_right, cv2.COLOR_GRAY2RGB)

                out_left.write(undistorted_left)
                out_right.write(undistorted_right)
        
                #display images
                cv2.imshow('Left Camera', undistorted_left)
                cv2.imshow('Right Camera', undistorted_right)

                if (cv2.waitKey(1) & 0xFF == ord('q')) | settings.exitFlag == True :
                    with settings.lock:
                        settings.exitFlag = True
                    break

        cv2.destroyAllWindows()

    def run(self):
        try:
            self.capture()
        except KeyboardInterrupt:
            sys.exit(0)
