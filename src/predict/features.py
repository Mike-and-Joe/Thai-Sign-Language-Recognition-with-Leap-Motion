import numpy as np
import json

def get_feature_tip_distance(data_amount):
    finger_name = ['thumb', 'index', 'middle', 'ring', 'pinky']

    tip_distance_amount = 5
    tip_distance = np.zeros([tip_distance_amount, data_amount])

    for file_no in range(data_amount): #read from each record
        with open("../record/one/json_{0}.txt".format(file_no)) as json_data:
            json_data = json.load(json_data)

        frame_amount = len(json_data)
        euclid_dist = np.zeros([tip_distance_amount, frame_amount])

        for frame_no, frame in enumerate(json_data):
            if not frame['hands']: #check if frame[hands] is null
                continue

            finger_tip = np.zeros([3, 5]) # [cooridinate x finger]

            for idx, finger in enumerate(finger_name):
                finger_tip[:, idx] = np.array(frame['hands']['right']['fingers'][finger]['bones']['distal']['next_joint'])

            for tip_distance_no in range (tip_distance_amount):
                curr_finger = finger_tip[:, tip_distance_no]
                next_finger = finger_tip[:, (tip_distance_no + 1) % 5]

                euclid_dist[tip_distance_no, frame_no] = np.linalg.norm(curr_finger - next_finger)

        euclid_dist_avg = euclid_dist.sum(axis=1) / frame_amount
        tip_distance[:, file_no] = euclid_dist_avg
        
    return tip_distance