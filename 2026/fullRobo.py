import serial
import time
import board
import pigpio
from checkTotem import viewTotem
from adafruit_motorkit import MotorKit

# Setup
kit = MotorKit(i2c=board.I2C())
pi = pigpio.pi()
if not pi.connected:
    exit()
    
servo_gpio = 4		

# Center servo
pi.set_servo_pulsewidth(servo_gpio,1000)
time.sleep(1)
pi.set_servo_pulsewidth(servo_gpio,0)


# Serial setup for Bluetooth
ser = serial.Serial("/dev/rfcomm0", 9600, timeout=1)
ser.reset_input_buffer()

# Initial motor speeds
speed_left = 0
speed_right = 0
kit.motor1.throttle = speed_left
kit.motor2.throttle = speed_right

# Duty cycles for servo directions
SERVO_CENTER = 1000
SERVO_RIGHT = 1150       
SERVO_LEFT = 850
SERVO_STOP = 0

try:
    while True:
        totem = viewTotem()
        print(totem)
        if totem != "no":
            if totem == "red":
                speed_left = speed_right = 0.99
                pi.set_servo_pulsewidth(servo_gpio,SERVO_CENTER)
                time.sleep(2)
                continue

            elif totem == "green":
                speed_left = speed_right = 0
                pi.set_servo_pulsewidth(servo_gpio,SERVO_CENTER)
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
           if line:
                try:
                   values = line.split(',')
                   if len(values) != 2:
                     continue
                   throttle = values[0]
                   direction = values[1]
                   print(throttle)
                   print(direction)
                     
                     #Stay in place
                   if throttle == "idle" and direction == "idle":
                      speed_left = speed_right = 0
                      servo_direction = SERVO_CENTER 
                    
                     # Control speed
                   throttle_val = int(throttle)
                   if throttle_val > 500 and throttle_val < 570:
                      speed_left = speed_right = 0
                   elif throttle_val > 512:
                      val = ((throttle_val - 512) / 512)
                      speed_left = speed_right = min(0.8, val)
                   elif throttle_val < 512:
                      val = -((512 - throttle_val) / 512)
                      speed_left = speed_right = max(-0.8, val)
                         
                  #Control direction
                   if direction == "left":
                         servo_direction = SERVO_LEFT
                     elif direction == "right":
                         servo_direction = SERVO_RIGHT
                     elif direction == "idle":
                         servo_direction = SERVO_CENTER
                     
                    #Apply motor speed
                     kit.motor1.throttle = -speed_left
                     kit.motor2.throttle = -speed_right
                    
                     print(-speed_left)
                    
                     #Apply motor direction
                     pi.set_servo_pulsewidth(servo_gpio, servo_direction)
                 
                except ValueError:
                    continue
                
        
except Exception:
    pi.set_servo_pulsewidth(servo_gpio, 0)  # Stop servo
    pi.stop()  # Disconnect pigpio
    pwm.stop()
    GPIO.cleanup()
    
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(servo_gpio, 0)  # Stop servo
    pi.stop()  # Disconnect pigpio
    pwm.stop()
    GPIO.cleanup()
