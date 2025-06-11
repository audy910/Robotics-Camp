import serial
import time
import board
import RPi.GPIO as GPIO
from checkTotem import viewTotem
from adafruit_motorkit import MotorKit

# Setup
kit = MotorKit(i2c=board.I2C())
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
pwm = GPIO.PWM(17, 50)
pwm.start(0)

# Center servo
pwm.ChangeDutyCycle(10)
time.sleep(0.3)
pwm.ChangeDutyCycle(0)

# Serial setup for Bluetooth
ser = serial.Serial("/dev/rfcomm0", 9600, timeout=1)
ser.reset_input_buffer()

# Initial motor speeds
speed_left = 0
speed_right = 0
kit.motor1.throttle = speed_left
kit.motor2.throttle = speed_right

# Duty cycles for servo directions
SERVO_CENTER = 8
SERVO_RIGHT = 6       
SERVO_LEFT = 10
SERVO_STOP = 0


try:
    while True:
        totem = viewTotem()
        print(totem)
        if totem != "no":
            if totem == "red":
                speed_left = speed_right = 0.99
                pwm.ChangeDutyCycle(SERVO_CENTER)
                time.sleep(2)
                continue

            elif totem == "green":
                speed_left = speed_right = 0
                pwm.ChangeDutyCycle(SERVO_CENTER)
                time.sleep(2)
                continue
            elif totem == "yellow":
                # Simulate turning behavior
                kit.motor1.throttle = 0.25
                kit.motor2.throttle = 0.5
                time.sleep(1)
                kit.motor1.throttle = 0.75
                kit.motor2.throttle = 0.5
                time.sleep(1)
                continue  # Skip the rest of the loop
        else:
            line = ser.read().decode("utf-8").strip()
            if line == "0":
                speed_left=speed_right = 0
            elif line == "1":
                speed_left = speed_right = 0.75
                pwm.ChangeDutyCycle(SERVO_CENTER)
                time.sleep(.2)
                pwm.ChangeDutyCycle(SERVO_STOP)
            elif line == "2":
                speed_left = 0.75
                speed_right = 0.5
                pwm.ChangeDutyCycle(SERVO_RIGHT)
                time.sleep(.2)
                pwm.ChangeDutyCycle(SERVO_STOP)
            elif line == "3":
                speed_left = 0.5
                speed_right = 0.75
                pwm.ChangeDutyCycle(SERVO_LEFT)
                time.sleep(.2)
                pwm.ChangeDutyCycle(SERVO_STOP)
            elif line == "4":
                speed_left = speed_right = -0.5
                pwm.ChangeDutyCycle(SERVO_CENTER)
                time.sleep(.2)
                pwm.ChangeDutyCycle(SERVO_STOP)
            

        # Apply motor speeds
        kit.motor1.throttle = speed_left
        kit.motor2.throttle = speed_right
                                                                                           
finally:
    pwm.stop()
    GPIO.cleanup()
