# Thomas Miles, 30/08/16
# tmiles@student.unimelb.edu.au
# 626263

"""   Contains basic control classes for basic robotics components:
       Servo __init__(self, pin, name, init = 2000)
       ESC __init__(self, pin, name)
       DCMotor __init__(self, fwdPin, revPin, name)
       An IO class is provided for neater GPIO control:
       IO __init__(self)
       Creating an object of this class by defult will activate the GPIO; This
       must be done before component classes are created
"""

import RPi.GPIO as GPIO
import time as t
import sys as sys
class IO:
    """ simplifys GPIO control """


    def __init__ (self):
        """ sets up the GPIO to defult settings """
        self.active = True
        self.warnings = False
        GPIO.setwarnings(self.warnings)
        GPIO.setmode(GPIO.BCM)

    def activate (self, yn):
        """ yn is a boolean input to activate/deactivate the GPIO """
        if self.active == yn:
            print "--> IO.active is already " + yn
        else:
            self.active = yn
            if self.active is True:
                GPIO.setwarnings(self.warnings)
                GPIO.setmode(GPIO.BCM)
                return
            elif self.active is False:
                GPIO.cleanup()
                print "--> IO has been disabled"
                return
            else:
                print "--> WARNING: IO.activate() requires a boolean input"
                return
#==============================================================================#


class Servo:
    """ for controling servo components """

    def __init__(self, pin, name, init):
        """ initialises servo """
        # init = defult angle

        GPIO.setup(pin, GPIO.OUT)
        self.channel = GPIO.PWM(pin, 100)# allocates GPIO channel, sets to 100Hz
        duty = float(init) / 3.6 # duty cycle for a given angle
        self.channel.start(duty)

        self.init = duty # saves defult duty cycle
        self.name = name
        print "--> " + name + " has been initialised"


    def reset(self):
        """ resets servo to defult position """

        self.channel.ChangeDutyCycle(self.init)
        print "--> "+ self.name + " has been reset"


    def setAngle(self, angle):
# Sets the servo to a given angle
        duty = float(angle) / 3.6
        self.channel.ChangeDutyCycle(duty)


    def deactivate (self):
        self.channel.stop()
        print "--> " + self.name + "has been deactivated"
#==============================================================================#


class DCMotor:
	""" Controls a dc motor through a L293D chip, also works for solenoids """

    def __init__ (self, fwdPin, revPin, name):
# When initialted, provide pin numbers for forward and reverse logic on GPIO

        self.name = name
        GPIO.setup(fwdPin, GPIO.OUT)
        GPIO.setup(revPin, GPIO.OUT)
        self.fwd = GPIO.PWM(fwdPin, 100) # sets output channels to 100Hz
        self.rev = GPIO.PWM(revPin, 100) #
        self.fwd.start(0)
        self.rev.start(0)

        print "--> " + self.name + " enabled"


    def setSpeed (self, speed):
        """ Speed is a percentage between -100 (reverse) and 100 """

        if speed > 0:
            if speed > 100:
                speed = 100
            self.rev.ChangeDutyCycle(0)
            self.fwd.ChangeDutyCycle(speed)

        elif speed < 0:
            if speed < -100:
                speed = -100
            self.fwd.ChangeDutyCycle(0)
            self.rev.ChangeDutyCycle(-speed)

        else:
            self.rev.ChangeDutyCycle(0)
            self.fwd.ChangeDutyCycle(0)

    def deactivate (self):
        self.rev.stop()
        self.fwd.stop()
        print "--> " + self.name + "has been deactivated"
#==============================================================================#


class ESC:
    """Sends signals to an electronic speed controler (ESC) in order to control
        a brushless DC motor
        __init__(self, pin, name):"""


    def __init__(self, pin, name):
        """ Sets up the ESC with a given GPIO pin """

        self.freq = 50 #Hz
        # duty values
        self.LOW = 7         # ~4000us
        self.NEUTURAL = 7.5  # ~6000us
        self.HIGH = 8   # ~8000us
        GPIO.setup(pin, GPIO.OUT)
        self.channel = GPIO.PWM(pin,self.freq)
        self.name = name
        self.duty = self.LOW
        self.channel.start(self.duty)
        self.pin = pin
        print "--> ESC channel setup\n"
		self.calibrate()


    def calibrate(self):
        """ calibrates the ESC """
        x = True
        while x:
        	keypress = raw_input (
                              "\n--> Initialising ESC on GPIO pin "
                              +str(self.pin)+
                              "\n\n   - Please ensure ESC is connected to GPIO."
                              "\n   - Connect the ESC to power and switch it on"
                              "\n   - Hold the SET button on the ESC."
                              "\n\n--> Hit enter to continue...\n"
                              )

        	keypress = raw_input ("  - When orange LED becomes solid, release "
                              "SET (should take ~4s)."
                              "\n\n--> Hit enter to continue...\n"
                          )
        	self.duty = self.HIGH
        	self.channel.ChangeDutyCycle(self.duty)
        	keypress = raw_input ("  - Red LED should flash and become solid,"
                            " motor should beep.\n"
                            "\n--> Hit enter to continue...\n")

        	self.duty = self.LOW
        	self.channel.ChangeDutyCycle(self.duty)
        	keypress = raw_input ("  - Orange LED should flash and become solid,"
                            " motor should beep twice.\n"
                            "\n--> Hit enter to continue...\n")

        	self.duty = self.NEUTURAL
        	self.channel.ChangeDutyCycle(self.duty)

        	keypress = raw_input ( "   - Both LEDs should blink and become solid.\n"
                        "   - Motor should then beep and the LEDs should wink"
                        "\n\n--> Hit enter to continue...\n")


            keypress = raw_input(
                            "--> Calibration complete, retry? (y/n): " )
            if keypress is "y":
				print "\n--> Please turn off ESC, calibration restarting.\n"
			else:
                print "\n--> Sucess confirmed, please restart ESC\n"
                x = False
#==============================================================================#


    def setSpeed(self, speed):
# Speed is a % between -100 (reverse) and 100
        if speed is 0:
            self.duty = self.NEUTURAL

        elif (speed > 100) or (speed < -100):
            print "--> ERROR: Invalid speed, must be between -100 and 100!"

        else:
            self.duty = self.NEUTURAL + (self.NEUTURAL-self.HIGH)*speed/100
            self.channel.ChangeDutyCycle(self.duty)
            print "--> " + self.name + " speed set to " + str(speed) + "%"
#==============================================================================#


    def deactivate (self):
        self.channel.stop()
        print "--> " + self.name + " has been deactivated"
