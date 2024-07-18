import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
IR_PIN = 22
GPIO.setup(IR_PIN, GPIO.OUT)

def transmit_signal():
    GPIO.output(IR_PIN, GPIO.HIGH)
    time.sleep(0.5)  
    GPIO.output(IR_PIN, GPIO.LOW)

try:
    while True:
        transmit_signal()
        time.sleep(2)  

except KeyboardInterrupt:
    GPIO.cleanup()

