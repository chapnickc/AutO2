
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

#Declare I/O
step = 18

enable =  24
direction = 23
freq = 1000         # lowest frequency

GPIO.setup(step, GPIO.OUT)
GPIO.setup(enable, GPIO.OUT)
GPIO.setup(direction, GPIO.OUT)

#Function
GPIO.output(enable, False) # or GPIO.HIGH instead of True 

# set the pwm to frequency to 1 kHz
pwm = GPIO.PWM(step, freq)

# sets the output to a 50% duty cycle
pwm.start(50)


for flip in range(5):
    GPIO.output(direction, True)
#    sleep(0.040)
#    GPIO.output(direction, False)


#sleep(5.5)
#sleep(10)

# turn off power to the pin , does not put low 
pwm.stop()

# turn off the enable pin  and the step pin
GPIO.output(step, False)
GPIO.output(enable, True)

GPIO.cleanup()
