import time, os

def create_folder(directory) :
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_last_index_from_folder(directory) :
    arr_txt = [int(x.split('.')[0].split('_')[1])
                for x in os.listdir(directory)
                if x.endswith(".txt")]

    if len(arr_txt):
        return max(arr_txt)
    else:
        return -1
