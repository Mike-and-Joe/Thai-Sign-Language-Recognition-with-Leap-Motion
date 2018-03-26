################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, thread, time, json, threading, time
from lib import Leap

import settings, main, utils

def get_list_from_vector (vector) :
    alist = []
    for index in range(3):
        alist.append(vector[index])
    return alist

class ApiRecorder():
    finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
    bone_names = ['metacarpal', 'proximal', 'intermediate', 'distal']
    path = ''
    export_data = []
    timer = utils.Timer()
    saved = True

    def set_is_open (self, value):
        with settings.lock:
            settings.is_open['leap_api'] = value

    def get_export_data (self) :
        return self.export_data

    def clear_export_data (self) :
        self.export_data = []

        return

    def transform_to_json (self, frame) :
        export_per_frame = {
            'frame_id': frame.id,
            'timestamp': frame.timestamp,
            'hand_available': len(frame.hands),
            'fingers': len(frame.fingers),
            'hands': {}
        }

        for hand in frame.hands:
            _hand = {}
            _hand['hand_id'] = hand.id

            _hand['hand_palm_position'] = get_list_from_vector(hand.palm_position)


            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            _hand.update({
                'pitch': direction.pitch * Leap.RAD_TO_DEG,
                'roll': normal.roll * Leap.RAD_TO_DEG,
                'yaw': direction.yaw * Leap.RAD_TO_DEG
            })

            # Get arm bone
            arm = hand.arm
            _hand['arm'] = {
                'direction': get_list_from_vector(arm.direction),
                'wrist_position': get_list_from_vector(arm.wrist_position),
                'elbow_position': get_list_from_vector(arm.elbow_position)
            }

            # Get fingers
            _fingers = {}
            for finger in hand.fingers:
                _finger = {
                    'id': finger.id,
                    'length': finger.length,
                    'widt': finger.width
                }

                # Get bones
                _bones = {}
                for b in range(0, 4):
                    bone = finger.bone(b)
                    bone_name = self.bone_names[bone.type]

                    _bones[bone_name] = {
                        'prev_joint': get_list_from_vector(bone.prev_joint),
                        'next_joint': get_list_from_vector(bone.next_joint),
                        'direction': get_list_from_vector(bone.direction)
                    }

                _finger['bones'] = _bones

                finger_name = self.finger_names[finger.type]
                _fingers[finger_name] = _finger

            _hand.update({ 'fingers': _fingers })

            _handType = "left" if hand.is_left else "right"
            # print _hand
            export_per_frame['hands'][_handType] = _hand
            # print export_per_frame
        return export_per_frame

    def getPath(self):
        return '/'.join(str(x) for x in [settings.path, settings.file_name, 'json_' + str(settings.file_index)]) + '.txt'

    def export_to_file (self):
        self.saved = True
        print ('export to file naja')
        with open(self.path, 'w') as out:
            res = json.dump(self.export_data, out, sort_keys=False, indent=2, separators=(',', ': '))

    def is_saved (self):
        return self.saved

    def export_frame_to_global (self, json_frame):
        if (self.timer.is_time_up(0.200)) :
            with settings.lock:
                settings.frame = json_frame

    def record (self, frame) :
        if not settings.is_open['leap_api']:
            self.saved = False
            self.path = self.getPath()
            print (self.path)
            self.clear_export_data()
            self.set_is_open(True)
            for key, value in settings.is_open.iteritems():
                print (key, value)



        json_frame = self.transform_to_json(frame)
        self.export_frame_to_global(json_frame)
        self.export_data.append(json_frame)


class SampleListener(Leap.Listener):
    api_recorder = ApiRecorder()

    def set_ready(self, is_ready):
        if not settings.is_ready['leap_api']:
            with settings.lock:
                settings.is_ready['leap_api'] = is_ready

    def on_exit(self, controller):
        self.set_ready(False)

    def on_connect(self, controller):
        self.set_ready(True)

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        self.set_ready(False)

    def on_frame(self, controller):
        frame = controller.frame()

        if settings.is_recording :
            self.api_recorder.record(frame)
        else :
            if not self.api_recorder.is_saved() :
                self.api_recorder.export_to_file()
                self.api_recorder.clear_export_data()
                self.api_recorder.set_is_open(False)
            else :
                json_frame = self.api_recorder.transform_to_json(frame)
                self.api_recorder.export_frame_to_global(json_frame)

class CaptureLeapApi(threading.Thread):
    listener = None

    def run(self):
        # Create a sample listener and controller
        self.listener = SampleListener()
        controller = settings.leap_controller

        # Have the sample listener receive events from the controller
        controller.add_listener(self.listener)


        while(not settings.exitFlag):
            time.sleep(0.100)
        self.stop()

    def stop(self):
        print "Trying to stop leap_api "
        controller = settings.leap_controller
        controller.remove_listener(self.listener)

        # thread.exit()

        if self.process is not None:
            # Release everything if job is finished

            self.process.terminate()
            self.process = None
