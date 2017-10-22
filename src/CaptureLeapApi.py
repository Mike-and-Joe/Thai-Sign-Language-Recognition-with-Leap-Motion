################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, thread, time, json, threading
from lib import Leap
from pprint import pprint

import settings

def get_list_from_vector (vector) :
    alist = []
    for index in range(3):
        alist.append(vector[index])
    return alist

def transform_to_json (frame) :
    export_data = {
        'frame_id': frame.id,
        'timestamp': frame.timestamp,
        'hand_available': len(frame.hands),
        'fingers': len(frame.fingers),
        'hands': {}
    }

    for hand in frame.hands:
        _hand = {}
        _hand['hand_type'] = "Left hand" if hand.is_left else "Right hand"
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
        _fingers = []
        for finger in hand.fingers:
            _finger = {
                'finger_name': self.finger_names[finger.type],
                'id': finger.id,
                'length': finger.length,
                'widt': finger.width
            }

            # Get bones
            _bones = []
            for b in range(0, 4):
                bone = finger.bone(b)
                _bones.append({
                    'bone_name': self.bone_names[bone.type],
                    'prev_joint': get_list_from_vector(bone.prev_joint),
                    'next_joint': get_list_from_vector(bone.next_joint),
                    'direction': get_list_from_vector(bone.direction)
                })
            _finger['bones'] = _bones

            _fingers.append(_finger)

        _hand.update({ 'fingers': _fingers })

        _handType = "left" if hand.is_left else "right"
        # print _hand
        export_data['hands'][_handType] = _hand
        # print export_data
    return export_data

path = ''

def record (frame) :
    if not settings.is_open['leap_api']:
        path = getPath()
        with settings.lock:
            settings.is_open['leap_api'] = True

    export_data = transform_to_json(frame)
    with open(path, 'a') as out:
        res = json.dump(export_data, out, sort_keys=False, indent=2, separators=(',', ': '))

def getPath(self):
    return '/'.join(str(x) for x in [settings.path, settings.file_name, 'facetime_' + str(settings.file_index)]) + '.avi'

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()

        if settings.is_recording :
            self.record(frame)

class CaptureLeapApi(threading.Thread):
    listener = None

    def run(self):
        # Create a sample listener and controller
        self.listener = SampleListener()
        controller = settings.leap_controller

        # Have the sample listener receive events from the controller
        controller.add_listener(self.listener)
        # controller.add_listener(self.listener)

    def stop(self):
        print "Trying to stop leap_api "
        controller = settings.leap_controller
        controller.remove_listener(self.listener)

        # thread.exit()

        if self.process is not None:
            # Release everything if job is finished

            self.process.terminate()
            self.process = None
