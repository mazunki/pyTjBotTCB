import RPi.GPIO as GPIO
import time

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

servo2PIN = 27
GPIO.setup(servo2PIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
q = GPIO.PWM(servo2PIN, 50) # GPIO 27 for PWM with 50Hz

# Initialization
p.start(2.5)
q.start(2.5)

try:
  while True:
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    q.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(10)
    time.sleep(0.5)
    q.ChangeDutyCycle(12.5)
    time.sleep(0.5)

except KeyboardInterrupt:
    p.stop()
    q.stop()
    GPIO.cleanup()
