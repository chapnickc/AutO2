class Motor:

    """ Motor Class which is responsible for turning the motor and keeping track of
        motor rotational position and thus current flow.

        We use the RPI number system where GPIO.BCM is broadcom-specific pin numberings.

        self._pos   - Holds the currents rotational position of the motor with the net number of steps taken.
    """
    
    import RPi.GPIO as GPIO
    import time

    FLOW = 24
    EN = 25
    DIR = 23
    STEP = 18
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor.EN, GPIO.out)
    GPIO.setup(Motor.DIR, GPIO.out)
    GPIO.setup(Motor.STEP, GPIO.out)
    GPIO.setup(Motor.FLOW, GPIO.input)
 #   GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def __init__(self):
        self._pos = 0
        self._flow = 0
        self._stepangle = 1.8
        self._rev = 360
        self._f = 1000
        self._DC = 50

    def calibrate(self):
        self._flow = GPIO.read(Motor.FLOW)

    def upFlow(self,steps):
        """ Increase the flow oxygen by rotating stepper motor specified number of steps."""

        GPIO.output(Motor.EN, GPIO.HIGH)      #Enable motor
        GPIO.output(Motor.DIR,GPIO.LOW)       #set direction

        self._pos = self._pos + steps
        pwm = GPIO.PWM(Motor.STEP,self._f)    # sets the pwm to frequency of 1kHz 
        pwm.start(self._DC)             # sets the output to a 50% duty cycle
        time.sleep(float(steps)/1000)   # no. of ms = no. of steps
        pwm.stop()
        GPIO.output(Motor.STEP,False)
        GPIO.output(Motor.EN,False)

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















