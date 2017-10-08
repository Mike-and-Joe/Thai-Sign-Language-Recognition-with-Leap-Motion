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
        global flag

        camera = 0
        cap = cv2.VideoCapture(camera)
        cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('./record/facetime_camera/output.avi',fourcc, 20.0, (cap_width,cap_height))

        while(cap.isOpened()):
            ret, frame = cap.read()

            if ret == True:
                frame = cv2.flip(frame, 1)

                # write the flipped frame
                out.write(frame)

                cv2.imshow('video output', frame)

                if (cv2.waitKey(1) & 0xFF == ord('q')) | settings.exitFlag == True :
                    with settings.lock:
                        settings.exitFlag = True
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()
