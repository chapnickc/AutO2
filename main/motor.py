from __future__ import division
import RPi.GPIO as GPIO
import time
from time import sleep

class Motor(object):

    """ Motor Class which is responsible for turning the motor and keeping track of
        motor rotational position and thus current flow.

        We use the RPI number system where GPIO.BCM is broadcom-specific pin numberings.

        self._pos   - Holds the currents rotational position of the motor with the net number of steps taken.
    """
    
#    import RPi.GPIO as GPIO
#    import time

#    FLOW = 24
    EN = 25                 #changed for Brian's board 04/26/2016
    DIR = 23 
    STEP = 24
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
#    GPIO.setup(FLOW, GPIO.input)
 #   GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def __init__(self):
        self._pos = 0
        self._flow = 0
        self._stepangle = 1.8
        self._rev = 360
        self._f = 1000
        self._DC = 50
        GPIO.output(Motor.EN, GPIO.LOW)      #Enable motor

    def calibrate(self):
        self._flow = GPIO.read(Motor.FLOW)

    def upFlow(self,steps):
        """ Increase the flow oxygen by rotating stepper motor specified number of steps."""


        GPIO.output(Motor.DIR,GPIO.LOW)       #set direction

        self._pos = self._pos + steps
        pwm = GPIO.PWM(Motor.STEP,self._f)    # sets the pwm to frequency of 1kHz 
        pwm.start(self._DC)             # sets the output to a 50% duty cycle
        time.sleep(float(steps)/self._f)   # no. of ms = no. of steps

        pwm.stop()
        GPIO.output(Motor.STEP,False)
 #       GPIO.output(Motor.EN,False)

    def downFlow(self,steps):
        """ Decrease the flow oxygen by rotating stepper motor specified number of steps."""

        GPIO.output(Motor.EN,GPIO.HIGH)       #Enable motor
        GPIO.output(Motor.DIR,GPIO.HIGH)      #set direction

        self._pos = self._pos - steps
        pwm = GPIO.PWM(Motor.STEP,self._f)    # sets the pwm to frequency of 1kHz 
        pwm.start(self._DC)             # sets the output to a 50% duty cycle
        time.sleep(float(steps)/1000)   # no. of ms = no. of steps
        pwm.stop()                      #For some reason does not pull STEP low
        GPIO.output(Motor.STEP,False)
        GPIO.output(Motor.EN,False)

    def enableMotor(self):
        GPIO.output(Motor.EN, True)

    def disableMotor(self):
        GPIO.output(Motor.EN, False)

    def shutdown(self):
        GPIO.cleanup()


class Motor2(Motor):
    def __init__(self):
        super(Motor2, self).__init__()
    

    def upFlow(self, steps):
        GPIO.output(Motor.EN,GPIO.LOW)       #enable the motor
        GPIO.output(Motor.DIR,GPIO.LOW)       #set direction

        self._pos = self._pos + steps

        for step in range(steps):
            GPIO.output(Motor.STEP, GPIO.LOW)
            sleep(5)
            print 'sleep is low'
            GPIO.output(Motor.STEP, GPIO.HIGH)
            sleep(5)
            print 'sleep is high'
            
        GPIO.output(Motor.STEP,False)
        GPIO.output(Motor.EN,GPIO.HIGH)       #enable the motor


    


if __name__ == '__main__':
    m = Motor2()
    m.upFlow(20)
    m.shutdown()
    










