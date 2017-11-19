import numpy as np
import json

def print_while_recording (frame):
    try:
        return get_finger_tip(frame)
    except Exception as e:
        return { }

def get_finger_tip(frame):
    finger_name = ['thumb', 'index', 'middle', 'ring', 'pinky']

    finger_tip = np.zeros([3, 5]) # [cooridinate x finger]

    for idx, finger in enumerate(finger_name):
        finger_tip[:, idx] = np.array(frame['hands']['right']['fingers'][finger]['bones']['distal']['next_joint'])

    return finger_tip

def get_feature_tip_distance(record_name, data_amount):
    tip_distance_amount = 5 * 5
    tip_distance = np.zeros([tip_distance_amount, data_amount])

    for file_no in range(data_amount): #read from each record
        try:
            with open("../record/{0}/json_{1}.txt".format(record_name, file_no)) as json_data:
                json_data = json.load(json_data)
        except Exception as e:
            print ('erro log:', record_name, file_no, Exception)
            raise

        frame_amount = len(json_data)
        euclid_dist = np.zeros([tip_distance_amount, frame_amount])

        for frame_no, frame in enumerate(json_data):
            if not 'hands' in frame or not 'right' in frame['hands'] : #check if frame[hands] is null
                print("../record/{0}/json_{1}.txt".format(record_name, file_no))
                print(frame_no)
                continue

            finger_tip = get_finger_tip(frame)

            for curr_idx in range(5):
                curr_finger = finger_tip[:, curr_idx]
                for comp_idx in range(5):
                    comp_finger = finger_tip[:, comp_idx]

                    euclid_dist[(curr_idx * 5) + comp_idx, frame_no] = np.linalg.norm(curr_finger - comp_finger)

            # for tip_distance_no in range (tip_distance_amount):
            #     curr_finger = finger_tip[:, tip_distance_no]
            #     next_finger = finger_tip[:, (tip_distance_no + 1) % 5]

            #     euclid_dist[tip_distance_no, frame_no] = np.linalg.norm(curr_finger - next_finger)

        euclid_dist_avg = euclid_dist.sum(axis=1) / frame_amount
        tip_distance[:, file_no] = euclid_dist_avg

    return tip_distance
