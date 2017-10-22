import time, os

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
