# this tutorial follows https://learn.sparkfun.com/tutorials/raspberry-gpio
# specifially, https://learn.sparkfun.com/tutorials/raspberry-gpio/python-rpigpio-api

import RPi.GPIO as GPIO

# to specify which number-system is being used
# you can use:
GPIO.setmode(GPIO.BCM)
#note that GPIO.BCM is the broadcom-specific pin numberings


GPIO.setup(18, GPIO.out) # if you want to use 18 as an output

#-------- Outputs ------------
# ___Digital Outputs______

# To write a pin high (to 3.3V) or low (to 0v), use
# GPIO.output([pin],[GPIO.LOW,GPIO.HIGH])
GPIO.output(18,GPIO.HIGH) # or GPIO.output(18, True)


#______ Analog Output ______
'''Pulse width modulation - about as limited as it can be..
#only pin 18 is capable
# to make script writing easier, you can assign an instance to a variable. ie.'''

pwm = GPIO.PWM(18,1000) # sets the pwm to frequency of 1kHz 
pwm.start(50) # sets the output to a 50% duty cycle

                # duty cycle is the cycle of operation
                # intermenttent rather than continuous

# to change the pwm output, for example to 75% output
pwm.ChangeDutyCycle(75)

# to turn pwm on the pin off
pwm.stop()

#-------------- Inputs -------------
'''If a pin is configured as an input, you can use the GPIO.input([pin]) to read its value
    # it will return either a true or false, depending on if it is HIGH or LOW'''

if GPIO.input(17)
    print('Pin 11 is HIGH')
else:
    print ('Pin 11 is LOW')

#---------------- Pull-Up/Down Resistors ------
'''Pull Up resistors are connected to high voltage and
 use a low amount of current to determine if the state
 of an input pin is high or low, and prevent misreads '''

# to Use a pull up resistor
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#------------ Delays -----------------
''' You can add delays to a python script. At the top of your script
you will need to write'''
import time

''' Then, throughout the rest of the script you can write
time.sleep([seconds])
'''
time.sleep(0.25)# sleep for 250 miliseconds

#------ Garbage Collecting ----
''' Once the script has run its course, be kind to the next proccess
that might use the GPIOs '''
GPIO.cleanup() # releases any resources the script may be using

















