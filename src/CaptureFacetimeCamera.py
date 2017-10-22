import cv2, threading, time

import settings, main

class CaptureFacetimeCamera(threading.Thread):
    cap = cv2.VideoCapture(1)
    cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    path = ''
    out = None

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.process = None
        self.name = name

    def set_is_open (self, value):
        with settings.lock:
            settings.is_open['facetime'] = value

    def set_ready(self, is_ready):
        if not settings.is_ready['facetime']:
            with settings.lock:
                settings.is_ready['facetime'] = is_ready

    def preparing(self):
        while not main.is_all_ready():
            ret, frame = self.cap.read()

            if ret == True:
                self.set_ready(True)
            else:
                self.set_ready(False)

            if settings.exitFlag == True:
                self.stop()
                break
            time.sleep(0.300)

    def ready(self):
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()

            if ret == True:
                frame = cv2.flip(frame, 1)
                cv2.imshow('Facetime', frame)

                # write the flipped frame
                if settings.is_recording :
                    self.record(frame)
                elif self.out and self.out.isOpened and self.out.isOpened():
                    self.out.release()
                    self.set_is_open(False)

                if main.wait_for_exit_key():
                    print 'Exit!'
                    break

            else:
                break

        self.stop()


    def record(self, frame):
        if not settings.is_open['facetime']:
            self.path = self.getPath()
            self.out = cv2.VideoWriter(self.path, self.fourcc, 20.0, (self.cap_width,self.cap_height))
            self.set_is_open(True)

        if not self.out.isOpened():
            # Define the codec and create VideoWriter object
            self.out.open(self.path, self.fourcc, 20.0, (self.cap_width,self.cap_height))

        self.out.write(frame)

    def getPath(self):
        return '/'.join(str(x) for x in [settings.path, settings.file_name, 'facetime_' + str(settings.file_index)]) + '.avi'

    def run(self):
        while(not settings.exitFlag):
            self.preparing()
            self.ready()
        self.stop()

    def stop(self):
        print "Trying to stop facetime "
        self.cap.release()
        cv2.destroyAllWindows()

        # thread.exit()

        if self.process is not None:
            # Release everything if job is finished

            self.process.terminate()
            self.process = None
