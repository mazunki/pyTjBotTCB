import RPi.GPIO as GPIO
import time

servoPIN = 20 
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 20 for PWM with 50Hz

# Initialization
def dance():
    p.start(2.5)

    while True:
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)

    else:
        p.stop()
        time.sleep(0.5)
        GPIO.cleanup()
