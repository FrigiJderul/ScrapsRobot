"""
Created on Wed Jan 22 17:29:51 2020

@author: Radu / TheFerridge

Scraps - the robot that... v1.02
"""

import pigpio
import time
import Pyro4

pi = pigpio.pi()

WhichWayFace = 1    #1 is facing forward, 2 is backward
ScrapsCoordinate = 0   # coordinates represent how many seconds it takes the bot to get to a room from base
CommonRoomCoordinate = 40
CentralOfficeCoordinate = 60
ReadingRoomCoordinate = 130
ObscureStudiesCoordinate = 68

sensor_switch = 0

motor_left_fwd = 12
motor_left_bck = 25
motor_right_fwd = 18
motor_right_bck = 24

left_arm_upwards = 19
left_arm_downwards = 13
right_arm_upwards = 6
right_arm_downwards = 5

pi.set_mode(motor_left_fwd, pigpio.OUTPUT)
pi.set_mode(motor_left_bck, pigpio.OUTPUT)
pi.set_mode(motor_right_fwd, pigpio.OUTPUT)
pi.set_mode(motor_right_bck, pigpio.OUTPUT)

pi.set_mode(left_arm_downwards, pigpio.OUTPUT)
pi.set_mode(left_arm_upwards, pigpio.OUTPUT)
pi.set_mode(right_arm_downwards, pigpio.OUTPUT)
pi.set_mode(right_arm_upwards, pigpio.OUTPUT)

pi.write(motor_left_bck, 0)  #just make sure everything is off
pi.write(motor_left_fwd, 0)
pi.write(motor_right_bck, 0)
pi.write(motor_right_fwd, 0)

pi.write(left_arm_upwards, 0)
pi.write(left_arm_downwards, 0)
pi.write(right_arm_upwards, 0)
pi.write(right_arm_downwards, 0)

def lift_left_arm ():
        pi.set_mode(left_arm_downwards, pigpio.OUTPUT)
        pi.set_mode(left_arm_upwards, pigpio.OUTPUT)
        pi.write(left_arm_upwards, 1)
        time.sleep(1)
        pi.write(left_arm_upwards, 0)
        time.sleep(2)
        pi.write(left_arm_downwards, 1)
        time.sleep(1)
        pi.write(left_arm_downwards, 0)
        print("I've lifted and put down my left arm!")

def lift_right_arm ():
        pi.set_mode(right_arm_downwards, pigpio.OUTPUT)
        pi.set_mode(right_arm_upwards, pigpio.OUTPUT)
        pi.write(right_arm_upwards, 1)
        time.sleep(1)
        pi.write(right_arm_upwards, 0)
        time.sleep(2)
        pi.write(right_arm_downwards, 1)
        time.sleep(1)
        pi.write(right_arm_downwards, 0)
        print("I've lifted and put down my right arm!")

@Pyro4.expose
class MoveIt (object):
    def go_origin (self, cop):
        global ScrapsCoordinate
        pi.set_mode(motor_left_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_left_bck, pigpio.OUTPUT)
        pi.set_mode(motor_right_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_right_bck, pigpio.OUTPUT)

        if ScrapsCoordinate == 0:
            return "You're already at the origin, dummy!"

        if WhichWayFace == 1:
            pi.write(motor_left_bck, 1)
            pi.write(motor_right_bck, 1)
            time.sleep(ScrapsCoordinate)
            pi.write(motor_left_bck, 0)
            pi.write(motor_right_bck, 0)
            ScrapsCoordinate = 0

        if WhichWayFace == 2:
            pi.write(motor_left_fwd, 1)
            pi.write(motor_right_fwd, 1)
            time.sleep(ScrapsCoordinate)
            pi.write(motor_left_fwd, 0)
            pi.write(motor_right_fwd, 0)
            ScrapsCoordinate = 0

    def go_common (self, cop):
        global ScrapsCoordinate
        pi.set_mode(motor_left_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_left_bck, pigpio.OUTPUT)
        pi.set_mode(motor_right_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_right_bck, pigpio.OUTPUT)

        if (CommonRoomCoordinate - ScrapsCoordinate) == 0:
            return "You're already at the Common Room, dummy!"

        if (CommonRoomCoordinate - ScrapsCoordinate) < 0:
            if WhichWayFace == 1:   #go backwards until you get there
                pi.write(motor_left_bck, 1)
                pi.write(motor_right_bck, 1)
                time.sleep(ScrapsCoordinate - CommonRoomCoordinate)
                pi.write(motor_left_bck, 0)
                pi.write(motor_right_bck, 0)
            if WhichWayFace == 2: #go forwards until you get there
                pi.write(motor_left_fwd, 1)
                pi.write(motor_right_fwd, 1)
                time.sleep(ScrapsCoordinate - CommonRoomCoordinate)
                pi.write(motor_left_fwd, 0)
                pi.write(motor_right_fwd, 0)

        if (CommonRoomCoordinate - ScrapsCoordinate) > 0:
            if WhichWayFace == 1:
                pi.write(motor_left_fwd, 1)
                pi.write(motor_right_fwd, 1)
                time.sleep(CommonRoomCoordinate - ScrapsCoordinate)
                pi.write(motor_left_fwd, 0)
                pi.write(motor_right_fwd, 0)
            if WhichWayFace == 2:
                pi.write(motor_left_bck, 1)
                pi.write(motor_right_bck, 1)
                time.sleep(CommonRoomCoordinate - ScrapsCoordinate)
                pi.write(motor_left_bck, 0)
                pi.write(motor_right_bck, 0)

        ScrapsCoordinate = CommonRoomCoordinate

        if WhichWayFace == 1:
            lift_right_arm()
        else:
            lift_left_arm()
        return ("Welcome to the Common Room!")

    def go_central (self, cop):
        global ScrapsCoordinate
        pi.set_mode(motor_left_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_left_bck, pigpio.OUTPUT)
        pi.set_mode(motor_right_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_right_bck, pigpio.OUTPUT)
        if (CentralOfficeCoordinate - ScrapsCoordinate) == 0:
            return "You're already at the Central Office, dummy!"

        if (CentralOfficeCoordinate - ScrapsCoordinate) < 0:
            if WhichWayFace == 1:   #go backwards until you get there
                pi.write(motor_left_bck, 1)
                pi.write(motor_right_bck, 1)
                time.sleep(ScrapsCoordinate - CentralOfficeCoordinate)
                pi.write(motor_left_bck, 0)
                pi.write(motor_right_bck, 0)
            if WhichWayFace == 2: #go forwards until you get there
                pi.write(motor_left_fwd, 1)
                pi.write(motor_right_fwd, 1)
                time.sleep(ScrapsCoordinate - CentralOfficeCoordinate)
                pi.write(motor_left_fwd, 0)
                pi.write(motor_right_fwd, 0)

        if (CentralOfficeCoordinate - ScrapsCoordinate) > 0:
            if WhichWayFace == 1:
                pi.write(motor_left_fwd, 1)
                pi.write(motor_right_fwd, 1)
                time.sleep(CentralOfficeCoordinate - ScrapsCoordinate)
                pi.write(motor_left_fwd, 0)
                pi.write(motor_right_fwd, 0)
            if WhichWayFace == 2:
                pi.write(motor_left_bck, 1)
                pi.write(motor_right_bck, 1)
                time.sleep(CentralOfficeCoordinate - ScrapsCoordinate)
                pi.write(motor_left_bck, 0)
                pi.write(motor_right_bck, 0)

        ScrapsCoordinate = CentralOfficeCoordinate

        if WhichWayFace == 1:
            lift_left_arm()
        else:
            lift_right_arm()

        return ("Welcome to the Central Office!")

    def go_read (self, cop):
        global ScrapsCoordinate
        pi.set_mode(motor_left_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_left_bck, pigpio.OUTPUT)
        pi.set_mode(motor_right_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_right_bck, pigpio.OUTPUT)
        if (ReadingRoomCoordinate - ScrapsCoordinate) == 0:
            return "You're already at the Reading Room, dummy!"

        if (ReadingRoomCoordinate - ScrapsCoordinate) < 0:
            if WhichWayFace == 1:   #go backwards until you get there
                pi.write(motor_left_bck, 1)
                pi.write(motor_right_bck, 1)
                time.sleep(ScrapsCoordinate - ReadingRoomCoordinate)
                pi.write(motor_left_bck, 0)
                pi.write(motor_right_bck, 0)
            if WhichWayFace == 2: #go forwards until you get there
                pi.write(motor_left_fwd, 1)
                pi.write(motor_right_fwd, 1)
                time.sleep(ScrapsCoordinate - ReadingRoomCoordinate)
                pi.write(motor_left_fwd, 0)
                pi.write(motor_right_fwd, 0)

        if (ReadingRoomCoordinate - ScrapsCoordinate) > 0:
            if WhichWayFace == 1:
                pi.write(motor_left_fwd, 1)
                pi.write(motor_right_fwd, 1)
                time.sleep(ReadingRoomCoordinate - ScrapsCoordinate)
                pi.write(motor_left_fwd, 0)
                pi.write(motor_right_fwd, 0)
            if WhichWayFace == 2:
                pi.write(motor_left_bck, 1)
                pi.write(motor_right_bck, 1)
                time.sleep(ReadingRoomCoordinate - ScrapsCoordinate)
                pi.write(motor_left_bck, 0)
                pi.write(motor_right_bck, 0)

        ScrapsCoordinate = ReadingRoomCoordinate

        if WhichWayFace == 1:
            lift_left_arm()
        else:
            lift_right_arm()

        return ("Welcome to the Reading Room!")

    def go_barry (self, cop):
        global ScrapsCoordinate
        pi.set_mode(motor_left_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_left_bck, pigpio.OUTPUT)
        pi.set_mode(motor_right_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_right_bck, pigpio.OUTPUT)
        if (ObscureStudiesCoordinate - ScrapsCoordinate) == 0:
            return "You're already at the office of the Chair of Obscure Studies, dummy!"

        if (ObscureStudiesCoordinate - ScrapsCoordinate) < 0:
            if WhichWayFace == 1:   #go backwards until you get there
                pi.write(motor_left_bck, 1)
                pi.write(motor_right_bck, 1)
                time.sleep(ScrapsCoordinate - ObscureStudiesCoordinate)
                pi.write(motor_left_bck, 0)
                pi.write(motor_right_bck, 0)
            if WhichWayFace == 2: #go forwards until you get there
                pi.write(motor_left_fwd, 1)
                pi.write(motor_right_fwd, 1)
                time.sleep(ScrapsCoordinate - ObscureStudiesCoordinate)
                pi.write(motor_left_fwd, 0)
                pi.write(motor_right_fwd, 0)

        if (ObscureStudiesCoordinate - ScrapsCoordinate) > 0:
            if WhichWayFace == 1:
                pi.write(motor_left_fwd, 1)
                pi.write(motor_right_fwd, 1)
                time.sleep(ObscureStudiesCoordinate - ScrapsCoordinate)
                pi.write(motor_left_fwd, 0)
                pi.write(motor_right_fwd, 0)
            if WhichWayFace == 2:
                pi.write(motor_left_bck, 1)
                pi.write(motor_right_bck, 1)
                time.sleep(ObscureStudiesCoordinate - ScrapsCoordinate)
                pi.write(motor_left_bck, 0)
                pi.write(motor_right_bck, 0)

        ScrapsCoordinate = ObscureStudiesCoordinate

        if WhichWayFace == 1:
            lift_right_arm()
        else:
            lift_left_arm()

        return "Welcome to the office of the Chair of Obscure Studies!"

    def turn_around (self, cop):
        global WhichWayFace
        pi.set_mode(motor_left_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_right_fwd, pigpio.OUTPUT)
        pi.write(motor_right_fwd, 1)
        time.sleep(3.2)
        pi.write(motor_right_fwd, 0)
        if WhichWayFace == 1:
            WhichWayFace = 2
        else:
            WhichWayFace = 1
        return "I've turned around!"

    def stop_everything (self, cop):
        pi.set_mode(motor_left_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_left_bck, pigpio.OUTPUT)
        pi.set_mode(motor_right_fwd, pigpio.OUTPUT)
        pi.set_mode(motor_right_bck, pigpio.OUTPUT)

        pi.set_mode(left_arm_downwards, pigpio.OUTPUT)
        pi.set_mode(left_arm_upwards, pigpio.OUTPUT)
        pi.set_mode(right_arm_downwards, pigpio.OUTPUT)
        pi.set_mode(right_arm_upwards, pigpio.OUTPUT)

        pi.write(motor_left_bck, 0)  #just make sure everything is off
        pi.write(motor_left_fwd, 0)
        pi.write(motor_right_bck, 0)
        pi.write(motor_right_fwd, 0)

        pi.write(left_arm_upwards, 0)
        pi.write(left_arm_downwards, 0)
        pi.write(right_arm_upwards, 0)
        pi.write(right_arm_downwards, 0)

        print ("Everything has been stopped.")

        return "Everything has been stopped."

    def self_destruct (self, cop):
        print("BOOM!")
        return "BOOM!"

    def check_motorleftfwd (self, cop):
        pi.set_mode(motor_left_fwd, pigpio.OUTPUT)
        pi.write(motor_left_fwd, 1)
        time.sleep(2)
        pi.write(motor_left_fwd, 0)
        return "Done."

    def check_motorleftbck (self, cop):
        pi.set_mode(motor_left_bck, pigpio.OUTPUT)
        pi.write(motor_left_bck, 1)
        time.sleep(2)
        pi.write(motor_left_bck, 0)
        return "Done."

    def check_motorrightfwd (self, cop):
        pi.set_mode(motor_right_fwd, pigpio.OUTPUT)
        pi.write(motor_right_fwd, 1)
        time.sleep(2)
        pi.write(motor_right_fwd, 0)
        return "Done."

    def check_motorrightbck (self, cop):
        pi.set_mode(motor_right_bck, pigpio.OUTPUT)
        pi.write(motor_right_bck, 1)
        time.sleep(2)
        pi.write(motor_right_bck, 0)
        return "Done."

    def sensor_on (self, cop):
        sensor_switch = 1

    def sensor_off (self, cop):
        sensor_switch = 0

    def set_to_origin (self, cop):
        global ScrapsCoordinate
        ScrapsCoordinate = 0
        return "Scraps is now at the origin"

    def set_to_orientation1 (self, cop):
        global WhichWayFace
        WhichWayFace = 1
        return "Which Way Face is now One"

Pyro4.Daemon.serveSimple(
        {
            MoveIt: "ScrapsServer"
        },
        host = '192.168.43.214',
        ns = True)

print ("Scraps Server is on! Let's do this!")
daemon.requestLoop()

