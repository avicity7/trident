import RPi.GPIO as GPIO
import time
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

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

lcd_columns = 16
lcd_rows = 2

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_backlight = digitalio.DigitalInOut(board.D4)

lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)

def display(text):
    lcd.clear()
    lcd.cursor_position(0, 0)# coloumn,row
    lcd.message = text


def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if (GPIO.input(C1) == 1):
        display(characters[0])
        time.sleep(debounce)
    if (GPIO.input(C2) == 1):
        display(characters[1])
        time.sleep(debounce)
    if (GPIO.input(C3) == 1):
        display(characters[2])
        time.sleep(debounce)
    if (GPIO.input(C4) == 1):
        display(characters[3])
        time.sleep(debounce)
    GPIO.output(line, GPIO.LOW)

while True:
    readLine(L1, ["1","2","3","A"])
    readLine(L2, ["4","5","6","B"])
    readLine(L3, ["7","8","9","C"])
    readLine(L4, ["*","0","#","D"])
