# -*- coding: utf-8 -*-
"""
Created on Sun Oct 08 12:21:05 2017

@author: Pakpoom
"""

import cv2
import threading

import settings

class CaptureFacetimeCamera(threading.Thread):
    def wait_for_ready(self):
        while(True):
            if not settings.is_ready['facetime']:
                with settings.lock:
                    settings.is_ready['facetime'] = True
            elif settings.is_ready['leap']:
                break

    def run(self):
        global flag

        camera = 0
        cap = cv2.VideoCapture(camera)
        cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('./record/facetime_camera/output.avi',fourcc, 20.0, (cap_width,cap_height))

        while(cap.isOpened()):
            if (not settings.is_ready['facetime']) | (not settings.is_ready['leap']):
                self.wait_for_ready()
            
            ret, frame = cap.read()

            if ret == True:
                frame = cv2.flip(frame, 1)

                cv2.imshow('video output', frame)

                # write the flipped frame
                if settings.is_recording:
                    cv2.waitKey(1)

                    if not out.isOpened():
                        # Define the codec and create VideoWriter object
                        out.open('./record/facetime_camera/output.avi',fourcc, 20.0, (cap_width,cap_height))
                    
                    out.write(frame)
                elif out.isOpened():
                    out.release()
                elif (cv2.waitKey(1) & 0xFF == ord('q')) | settings.exitFlag == True :
                    with settings.lock:
                        settings.exitFlag = True
                    break
                
            else:
                break

        # Release everything if job is finished
        cap.release()
        cv2.destroyAllWindows()
