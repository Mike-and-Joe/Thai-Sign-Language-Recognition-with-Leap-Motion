import numpy as np
import pandas as pd
import json

def get_finger_tip(frame):
    finger_name = ['thumb', 'index', 'middle', 'ring', 'pinky']

    finger_tip = np.zeros([3, 5]) # [cooridinate x finger]

    for idx, finger in enumerate(finger_name):
        finger_tip[:, idx] = np.array(frame['hands']['right']['fingers'][finger]['bones']['distal']['next_joint'])
    
    return finger_tip

def get_feature_tip_distance(record_folder, record_name, data_amount):
    # tip_distance_amount = 5 * 5
    orig = dest = ['t', 'i', 'm', 'r', 'p']
    # tip_distance = np.zeros([data_amount, tip_distance_amount])
    euclid_dists = pd.DataFrame(columns=['tt','ti','tm','tr','tp'
                    ,'it','ii','im','ir','ip'
                    ,'mt','mi','mm','mr','mp'
                    ,'rt','ri','rm','rr','rp'
                    ,'pt','pi','pm','pr','pp'
                    ,'label'])

    for file_no in range(data_amount): #read from each record
        try:
            with open("../{0}/{1}/json_{2}.txt".format(record_folder, record_name, file_no)) as json_data:
                json_data = json.load(json_data)
        except Exception as s:
            print ('error log:', record_name, file_no, s)
            continue

        # frame_amount = len(json_data)
        euclid_dist = {}
        euclid_dist_frames = pd.DataFrame(columns=['tt','ti','tm','tr','tp'
                        ,'it','ii','im','ir','ip'
                        ,'mt','mi','mm','mr','mp'
                        ,'rt','ri','rm','rr','rp'
                        ,'pt','pi','pm','pr','pp'])
        # euclid_dist = np.zeros([tip_distance_amount, frame_amount])

        finger_tip = {}
        for frame_no, frame in enumerate(json_data):
            if not frame['hands'] or not 'right' in frame['hands']: #check if frame[hands] is null or left #check if frame[hands][right] is undefined
                continue

            finger_tip = get_finger_tip(frame)
            
            for curr_idx, curr_val in enumerate(orig):
                curr_finger = finger_tip[:, curr_idx]
                for dest_idx, dest_val in enumerate(dest):
                    comp_finger = finger_tip[:, dest_idx]
                    euclid_dist[curr_val + dest_val] = np.linalg.norm(curr_finger - comp_finger)
            
            # euclid_dist['label'] = record_name
            euclid_dist_frames = euclid_dist_frames.append(euclid_dist, ignore_index=True)
            
                
            # for curr_idx in range(5):
            #     curr_finger = finger_tip[:, curr_idx]
            #     for comp_idx in range(5):
            #         comp_finger = finger_tip[:, comp_idx]

            #         euclid_dist[(curr_idx * 5) + comp_idx, frame_no] = np.linalg.norm(curr_finger - comp_finger)
        
        if len(finger_tip) == 0:
            continue

        for curr_idx, curr_val in enumerate(orig):
            curr_finger = finger_tip[:, curr_idx]
            for dest_idx, dest_val in enumerate(dest):
                comp_finger = finger_tip[:, dest_idx]
                euclid_dist[curr_val + dest_val] = np.linalg.norm(curr_finger - comp_finger)

        euclid_dist_row = {
            curr_val+dest_val: euclid_dist_frames[curr_val+dest_val].mean() 
            for curr_val in orig 
            for dest_val in dest
        }

        euclid_dist_row['label'] = record_name
        euclid_dists = euclid_dists.append(euclid_dist_row, ignore_index=True)
        # euclid_dist_avg = euclid_dist.sum(axis=1) / frame_amount
        # tip_distance[file_no, :] = euclid_dist_avg
    
    return euclid_dists
    # return tip_distance

    def build_model(data_length, label_length):
        right_thumb_x = Input(shape=(data_length, 1), name='right_thumb_x')
        right_thumb_y = Input(shape=(data_length, 1), name='right_thumb_y')
        right_thumb_z = Input(shape=(data_length, 1), name='right_thumb_z')
        right_index_y = Input(shape=(data_length, 1), name='right_index_y')
        right_index_x = Input(shape=(data_length, 1), name='right_index_x')
        right_index_z = Input(shape=(data_length, 1), name='right_index_z')
        right_middle_x = Input(shape=(data_length, 1), name='right_middle_x')
        right_middle_y = Input(shape=(data_length, 1), name='right_middle_y')
        right_middle_z = Input(shape=(data_length, 1), name='right_middle_z')
        right_ring_x = Input(shape=(data_length, 1), name='right_ring_x')
        right_ring_y = Input(shape=(data_length, 1), name='right_ring_y')
        right_ring_z = Input(shape=(data_length, 1), name='right_ring_z')
        right_pinky_x = Input(shape=(data_length, 1), name='right_pinky_x')
        right_pinky_y = Input(shape=(data_length, 1), name='right_pinky_y')
        right_pinky_z = Input(shape=(data_length, 1), name='right_pinky_z')
        left_thumb_x = Input(shape=(data_length, 1), name='left_thumb_x')
        left_thumb_y = Input(shape=(data_length, 1), name='left_thumb_y')
        left_thumb_z, = Input(shape=(data_length, 1), name='left_thumb_z')
        left_index_x = Input(shape=(data_length, 1), name='left_index_x')
        left_index_y = Input(shape=(data_length, 1), name='left_index_y')
        left_index_z, = Input(shape=(data_length, 1), name='left_index_z')
        left_middle_x = Input(shape=(data_length, 1), name='left_middle_x')
        left_middle_y = Input(shape=(data_length, 1), name='left_middle_y')
        left_middle_z = Input(shape=(data_length, 1), name='left_middle_z')
        left_ring_x = Input(shape=(data_length, 1), name='left_ring_x')
        left_ring_y = Input(shape=(data_length, 1), name='left_ring_y')
        left_ring_z = Input(shape=(data_length, 1), name='left_ring_z')
        left_pinky_x = Input(shape=(data_length, 1), name='left_pinky_x')
        left_pinky_y = Input(shape=(data_length, 1), name='left_pinky_y')
        left_pinky_z = Input(shape=(data_length, 1), name='left_pinky_z')

        right_thumb_x_layers = LSTM(16, return_sequences=False)(right_thumb_x)
        right_thumb_y_layers = LSTM(16, return_sequences=False)(right_thumb_y)
        right_thumb_z_layers = LSTM(16, return_sequences=False)(right_thumb_z)
        right_index_y_layers = LSTM(16, return_sequences=False)(right_index_y)
        right_index_x_layers = LSTM(16, return_sequences=False)(right_index_x)
        right_index_z_layers = LSTM(16, return_sequences=False)(right_index_z)
        right_middle_x_layers = LSTM(16, return_sequences=False)(right_middle_x)
        right_middle_y_layers = LSTM(16, return_sequences=False)(right_middle_y)
        right_middle_z_layers = LSTM(16, return_sequences=False)(right_middle_z)
        right_ring_x_layers = LSTM(16, return_sequences=False)(right_ring_x)
        right_ring_y_layers = LSTM(16, return_sequences=False)(right_ring_y)
        right_ring_z_layers = LSTM(16, return_sequences=False)(right_ring_z)
        right_pinky_x_layers = LSTM(16, return_sequences=False)(right_pinky_x)
        right_pinky_y_layers = LSTM(16, return_sequences=False)(right_pinky_y)
        right_pinky_z_layers = LSTM(16, return_sequences=False)(right_pinky_z)
        left_thumb_x_layers = LSTM(16, return_sequences=False)(left_thumb_x)
        left_thumb_y_layers = LSTM(16, return_sequences=False)(left_thumb_y)
        left_thumb_z_layers, =LSTM(16, return_sequences=False)(left_thumb_z)
        left_index_x_layers = LSTM(16, return_sequences=False)(left_index_x)
        left_index_y_layers = LSTM(16, return_sequences=False)(left_index_y)
        left_index_z_layers, =LSTM(16, return_sequences=False)(left_index_z)
        left_middle_x_layers = LSTM(16, return_sequences=False)(left_middle_x)
        left_middle_y_layers = LSTM(16, return_sequences=False)(left_middle_y)
        left_middle_z_layers = LSTM(16, return_sequences=False)(left_middle_z)
        left_ring_x_layers = LSTM(16, return_sequences=False)(left_ring_x)
        left_ring_y_layers = LSTM(16, return_sequences=False)(left_ring_y)
        left_ring_z_layers = LSTM(16, return_sequences=False)(left_ring_z)
        left_pinky_x_layers = LSTM(16, return_sequences=False)(left_pinky_x)
        left_pinky_y_layers = LSTM(16, return_sequences=False)(left_pinky_y)
        left_pinky_z_layers = LSTM(16, return_sequences=False)(left_pinky_z)

        output = concatenate(
            [
                right_thumb_x_layers,
                right_thumb_y_layers,
                right_thumb_z_layers,
                right_index_y_layers,
                right_index_x_layers,
                right_index_z_layers,
                right_middle_x_layers,
                right_middle_y_layers,
                right_middle_z_layers,
                right_ring_x_layers,
                right_ring_y_layers,
                right_ring_z_layers,
                right_pinky_x_layers,
                right_pinky_y_layers,
                right_pinky_z_layers,
                left_thumb_x_layers,
                left_thumb_y_layers,
                left_thumb_z_layers,
                left_index_x_layers,
                left_index_y_layers,
                left_index_z_layers,
                left_middle_x_layers,
                left_middle_y_layers,
                left_middle_z_layers,
                left_ring_x_layers,
                left_ring_y_layers,
                left_ring_z_layers,
                left_pinky_x_layers,
                left_pinky_y_layers,
                left_pinky_z_layers
            ]
        )

        output = Dense(38, activation='softmax', name='combine_input')(output)

        model = Model(
            inputs = [
                right_thumb_x,
                right_thumb_y,
                right_thumb_z,
                right_index_y,
                right_index_x,
                right_index_z,
                right_middle_x,
                right_middle_y,
                right_middle_z,
                right_ring_x,
                right_ring_y,
                right_ring_z,
                right_pinky_x,
                right_pinky_y,
                right_pinky_z,
                left_thumb_x,
                left_thumb_y,
                left_thumb_z,
                left_index_x,
                left_index_y,
                left_index_z,
                left_middle_x,
                left_middle_y,
                left_middle_z,
                left_ring_x,
                left_ring_y,
                left_ring_z,
                left_pinky_x,
                left_pinky_y,
                left_pinky_z
            ], 
            outputs = [
                output
            ]
        )

        model.compile(
            loss='categorical_crossentropy',
            optimizer='sgd',
            metrics=['accuracy']
        )

        return model

        features['right_thumb_x']
        features['right_thumb_y']
        features['right_thumb_z']
        features['right_index_y']
        features['right_index_x']
        features['right_index_z']
        features['right_middle_x']
        features['right_middle_y']
        features['right_middle_z']
        features['right_ring_x']
        features['right_ring_y']
        features['right_ring_z']
        features['right_pinky_x']
        features['right_pinky_y']
        features['right_pinky_z']
        features['left_thumb_x']
        features['left_thumb_y']
        features['left_thumb_z']
        features['left_index_x']
        features['left_index_y']
        features['left_index_z']
        features['left_middle_x']
        features['left_middle_y']
        features['left_middle_z']
        features['left_ring_x']
        features['left_ring_y']
        features['left_ring_z']
        features['left_pinky_x']
        features['left_pinky_y']
        features['left_pinky_z']