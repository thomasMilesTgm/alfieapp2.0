
# Thomas Miles, 30/08/16
# tmiles@student.unimelb.edu.au
# 626263
from control import *
import sys as sys
class Alfie:
    """ Class used to impliment the entire robot """

    def __init__(self):
        self.IO = IO()
        self.steering_servo = Servo(14, "Steering Servo", 35)   #GPIO pin 14
        self.arm_servo = Servo(15, "Arm Servo", 90)             #GPIO pin 15
        self.release_servo = Servo(18, "Release Servo", 1)     #GPIO pin 18
        self.drive_esc = ESC(25, "Drive ESC")                  #GPIO pin 25


    def resetServos(self):
        self.steering_servo.reset()
        self.arm_servo.reset()
        self.release_servo.reset()

    def release(self):
        """ Actuates the release mechanism """

        self.release_servo.setAngle(180)

    def lift(self):
        """ Actuates the arm shortening mechanism """

        self.arm_servo.setAngle(45)


    def stage1(self,t1,speed):
	self.drive_esc.setSpeed(speed)
	t.sleep(t1)


    def stage2(self,t2,angle):
	self.steering_servo.setAngle(angle)
	t.sleep(t2)
	self.steering_servo.reset()

    def stage3(self,t3):
	t.sleep(t3)

    def stage4(self,t4,angle):
	self.steering_servo.setAngle(angle)
	t.sleep(t4)
	self.steering_servo.reset()

    def stage5(self,t5):
	if t5 is True:
	    self.lift()

    def stage6(self,t6):
	self.drive_esc.setSpeed(0)
	t.sleep(t6)


    def stage7(self,t7,restart_speed):
	if t7 is True:
	    self.release()
	    t.sleep(0.5)
	    self.drive_esc.setSpeed(restart_speed)

    def stage8(self,t8,angle):
	self.steering_servo.setAngle(angle)
	t.sleep(t8)
	self.steering_servo.reset()

    def stage9(self,t9):
	t.sleep(t9)

    def stage10(self,t10):
        self.drive_esc.setSpeed(0)
		t.sleep(t10)

    def terminate(self):
        self.steering_servo.deactivate()
        self.arm_servo.deactivate()
        self.release_servo.deactivate()
        self.drive_esc.deactivate()
        self.IO.activate(False)
        sys.exit("--> All objects deactivated goodbye!")
