# -*- coding: utf-8 -*-
"""
Created on Sun Oct 08 12:21:05 2017

@author: Pakpoom
"""

import cv2
import threading

import settings

class CaptureFacetimeCamera(threading.Thread):
    def run(self):
        camera = 1
        cap = cv2.VideoCapture(camera)
        print cap.isOpened()
        print cap.get(3)

        while True:
            ret, img = cap.read()

            if ret == True:
                fImg = cv2.flip(img, 1)
                cv2.imshow('video output', fImg)

                if (cv2.waitKey(1) & 0xFF == ord('q')) | settings.exitFlag == True :
                    with settings.lock:
                        settings.exitFlag = True
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()
