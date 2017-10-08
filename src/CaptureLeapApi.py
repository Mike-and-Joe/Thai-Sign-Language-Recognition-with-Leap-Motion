################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, thread, time, json
from lib import Leap
from pprint import pprint

import settings

def get_list_from_vector (vector) :
    alist = []
    for index in range(3):
        alist.append(vector[index])
    return alist

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

        with open('data.txt', 'a') as out:
            res = json.dump(export_data, out, sort_keys=False, indent=2, separators=(',', ': '))

    # def on_frame(self, controller):
    #     # Get the most recent frame and report some basic information
    #     frame = controller.frame()
    #
    #     print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
    #           frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
    #
    #     # Get hands
        # for hand in frame.hands:
    #
    #         handType = "Left hand" if hand.is_left else "Right hand"
    #
    #         print "  %s, id %d, position: %s" % (
    #             handType, hand.id, hand.palm_position)
    #
    #         # Get the hand's normal vector and direction
    #         normal = hand.palm_normal
    #         direction = hand.direction
    #
    #         # Calculate the hand's pitch, roll, and yaw angles
    #         print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
    #             direction.pitch * Leap.RAD_TO_DEG,
    #             normal.roll * Leap.RAD_TO_DEG,
    #             direction.yaw * Leap.RAD_TO_DEG)
    #
    #         # Get arm bone
    #         arm = hand.arm
    #         print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
    #             arm.direction,
    #             arm.wrist_position,
    #             arm.elbow_position)
    #
    #         # Get fingers
    #         for finger in hand.fingers:
    #
    #             print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
    #                 self.finger_names[finger.type],
    #                 finger.id,
    #                 finger.length,
    #                 finger.width)
    #
    #             # Get bones
    #             for b in range(0, 4):
    #                 bone = finger.bone(b)
    #                 print "      Bone: %s, start: %s, end: %s, direction: %s" % (
    #                     self.bone_names[bone.type],
    #                     bone.prev_joint,
    #                     bone.next_joint,
    #                     bone.direction)
    #
    #     if not frame.hands.is_empty:
    #         print ""

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = settings.leap_controller

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    while settings.exitFlag == False:
        pass

    controller.remove_listener(listener)

if __name__ == "__main__":
    main()
