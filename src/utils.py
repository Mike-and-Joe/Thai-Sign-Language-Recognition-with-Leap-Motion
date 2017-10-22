import cv2, time, os
import settings

def wait_for_ready(_self):
    while(True):
        if all(item for item in settings.is_ready):
            break
        if settings.exitFlag == True:
            _self.stop()
        time.sleep(0.100)

def wait_for_exit_key():
    if (cv2.waitKey(1) & 0xFF == ord('q')) | settings.exitFlag == True :
        with settings.lock:
            settings.exitFlag = True
        return True
    else:
        return False

def create_folder(directory) :
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_last_index_from_folder(directory) :
    arr_txt = [x for x in os.listdir(directory) if x.endswith(".txt")]
    if len(arr_txt):
        return int(
            arr_txt[len(arr_txt)-1]
            .split('.')[0]
            .split('_')[1]
        )
    else:
        return -1
