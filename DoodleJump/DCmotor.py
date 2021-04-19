import RPi.GPIO as GPIO  #imports the GPIO module
from time import sleep   #imports sleep

GPIO.setmode(GPIO.BOARD) #sets pin numbering to BOARD numbering system

GPIO.setup(29, GPIO.OUT) #sets up GPIO5 (pin 29) as out (INPUT 1)
GPIO.setup(31, GPIO.OUT) #GPIO 31                       (INPUT 2)
GPIO.setup(33, GPIO.OUT) #GPIO 33                       (ENABLE)

pwm = GPIO.PWM(33,200)    #setting up the PWN command type
pwm.start(0)              #starts the PWM with 0 duty so no run
#finally:
#    pwm.stop()
#    GPIO.cleanup()


#setting the motor to run forward at 50% power for 2 seconds
try:
    GPIO.output(29, True)
    GPIO.output(31, False)

    pwm.ChangeDutyCycle(100)

    GPIO.output(33, True)
    sleep(2)
    GPIO.output(33, False)
    
finally:
    pwm.stop()
    GPIO.cleanup()
    
    
    
