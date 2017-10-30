import json
import numpy as np

with open('../record/one/json_10.txt') as json_data:
    json_data = json.load(json_data)


feature_amount = 5
frame_amount = len(json_data)
euclid_dist = np.zeros([frame_amount,feature_amount])
finger_name = ['thumb', 'index', 'middle', 'ring', 'pinky']

for frame_no, frame in enumerate(json_data):
    if not frame['hands']:
        continue

    finger_tip = np.zeros([3, 5])

    for idx, finger in enumerate(finger_name):
        finger_tip[:, idx] = np.array(frame['hands']['right']['fingers'][finger]['bones']['distal']['next_joint'])

    for feature_no in range (feature_amount):
        curr_finger = finger_tip[:, feature_no]
        next_finger = finger_tip[:, (feature_no + 1) % 5]
        euclid_dist[frame_no, feature_no] = np.linalg.norm(curr_finger - next_finger)

euclid_dist_avg = euclid_dist.sum(axis=0) / frame_amount
print(euclid_dist_avg)