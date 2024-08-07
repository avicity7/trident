import RPi.GPIO as GPIO
import time

L1 = 5
L2 = 7
L3 = 6
L4 = 13

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

debounce = 0.2

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        print(characters[0])
        time.sleep(debounce)
    if(GPIO.input(C2) == 1):
        print(characters[1])
        time.sleep(debounce)
    if(GPIO.input(C3) == 1):
        print(characters[2])
        time.sleep(debounce)
    if(GPIO.input(C4) == 1):
        print(characters[3])
        time.sleep(debounce)
    GPIO.output(line, GPIO.LOW)

try:
    while True:
        readLine(L1, ["1","2","3","A"])
        readLine(L2, ["4","5","6","B"])
        readLine(L3, ["7","8","9","C"])
        readLine(L4, ["*","0","#","D"])
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nApplication stopped!")
