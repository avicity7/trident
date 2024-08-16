import smbus					#import SMBus module of I2C
import threading
import requests
import socketio
import os
import RPi.GPIO as GPIO
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from dotenv import load_dotenv
load_dotenv() 
from lirc import RawConnection

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

conn = RawConnection()

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


#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	bus.write_byte_data(Device_Address, CONFIG, 0)
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
  #Accelero and Gyro value are 16-bit
  high = bus.read_byte_data(Device_Address, addr)
  low = bus.read_byte_data(Device_Address, addr+1)  

  value = ((high << 8) | low)
  
  #to get signed value from mpu6050
  if(value > 32768):
          value = value - 65536
  return value


bus = smbus.SMBus(1)
Device_Address = 0x68

MPU_Init()

inBattle = False
sentBattle = False
backend_uri = os.environ["BACKEND_URI"]
cad_id = os.environ["CAD_ID"]
uid = ""
battle_id = ""
win = False
sending = False

inp = ""
hp = 100
psions = 100

Ax, Ay, Gx = 0,0,0

def getUserId():
  global uid 
  r = requests.get(f'{backend_uri}/cad/get-link?cad_id={cad_id}')
  uid = r.json()[0][0]

def checkInBattle():
  global inBattle, battle_id
  r = requests.get(f'{backend_uri}/battle/get-current-battle?uid={uid}')
  data = r.json()
  if len(data) > 0:
    battle_id = data[0][0]
    inBattle = True
    refreshMagicianState()
  else:
    inBattle = False
    

ot1 = ""
ot2 = ""
def display(t1, t2=""):
  global ot1, ot2
  if t1 != ot1 or t2 != ot2:
    lcd.clear()
    lcd.cursor_position(0, 0)# column,row
    lcd.message = t1
    lcd.cursor_position(0, 1)
    lcd.message = t2
    ot1 = t1
    ot2 = t2

def read6axis():
  global Ax, Ay, Gx
  acc_x = read_raw_data(ACCEL_XOUT_H)
  acc_y = read_raw_data(ACCEL_YOUT_H)
  gyro_x = read_raw_data(GYRO_XOUT_H)

  Ax = acc_x/16384.0
  Ay = acc_y/16384.0
  Gx = gyro_x/131.0

def readLine(line, characters):
	global inp
	GPIO.output(line, GPIO.HIGH)
	if (GPIO.input(C1) == 1):
		inp += characters[0]
		time.sleep(debounce)
	if (GPIO.input(C2) == 1):
		inp += characters[1]
		time.sleep(debounce)
	if (GPIO.input(C3) == 1):
		inp += characters[2]
		time.sleep(debounce)
	if (GPIO.input(C4) == 1):
		inp += characters[3]
		time.sleep(debounce)
	GPIO.output(line, GPIO.LOW)

def readNumpad():
  readLine(L1, ["1","2","3","A"])
  readLine(L2, ["4","5","6","B"])
  readLine(L3, ["7","8","9","C"])
  readLine(L4, ["*","0","#","D"])

def processIRRemote():
  try:
    keypress = conn.readline(.0001)
  except:
    keypress=""
          
  if (keypress != "" and keypress != None):
    data = keypress.split()
    sequence = data[1]
    command = data[2]

    if (sequence != "00"):
      return None
    
    return command

def refreshMagicianState():
  global hp, psions, inBattle
  r = requests.get(f'{backend_uri}/magician/get-state?user_id={uid}')
  data = r.json()[0]
  hp = data[1]
  psions = data[2]
  if hp <= 0:
    display("YOU LOST")
    time.sleep(10)
    inBattle = False
  else:
    display(f'HP: {hp} PSI: {psions}')

def createBattle():
  global inp
  obj = {"p2": uid}
  r = requests.post(f'{backend_uri}/battle/create-battle', json=obj)
  data = r.json()
  display("INCOMING BATTLE", str(data[1]))

  inp = ""

def acceptBattle():
  global sentBattle, uid, inp
  obj = {"confirmation": inp[:-1], "uid": uid}  
  r = requests.post(f'{backend_uri}/battle/accept-battle', json=obj)
  data = r.json()
  if data[0] == "OK":
    checkInBattle()
    sentBattle = False
  else:
    display("WRONG BATTLE", "CODE")
    time.sleep(2)
    sentBattle = False
  
  inp = ""

def createEvent():
  global uid, battle_id, inp, sending, Ax, Ay, Gx
  if not sending: 
    sending = True
    code = inp[:-1]
    obj = {"emitter": uid, "event_id": code, "battle_id": battle_id}
    r = requests.post(f'{backend_uri}/event/create-event', json=obj)
    data = r.json()
    if data[0] == "OK":
      os.system('irsend --device=/var/run/lirc/lircd-tx SEND_ONCE epson Power')
      display(data[1], "casted!")
      time.sleep(2)
      refreshMagicianState()
    else:
      display("INCORRECT MAGIC", "SEQUENCE")
      time.sleep(0.5)

  inp = ""
  Ax = 0
  Ay = 0
  Gx = 0 

def processEvent():
  obj = {"battle_id": battle_id, "uid": uid}
  requests.post(f'{backend_uri}/event/process-event', json=obj)

def sendBattle():
  global inp, sentBattle 
  os.system('irsend --device=/var/run/lirc/lircd-tx SEND_ONCE epson Source')

  inp = ""
  sentBattle = True


getUserId()
checkInBattle()


def main():
  global inBattle, sentBattle, inp, win, sending, ot1
  while True:
    if not win:
      if inBattle:
        tx = processIRRemote()
        if tx == "Power" and not sending:
          processEvent()
        else:
          sending = False
          readNumpad()
          if ot1 != "INCORRECT MAGIC":
            display(ot1, inp)
          else:
            display(f'HP: {hp} PSI: {psions}', inp)
          if inp != "":
            if inp[-1] == "A":
              while not Ax > 1.2:
                display("PUSH ARM")
                read6axis()
              createEvent()
            elif inp[-1] == "C":
              inp = inp[:-2]
            elif inp[-1] == "D":
              inp = ""

      elif sentBattle:
        display("ENTER CODE", inp)
        readNumpad()
        if inp != "":
          if inp[-1] == "A":
            acceptBattle()
          elif inp[-1] == "C":
            inp = inp[:-2]
          elif inp[-1] == "D":
            sentBattle = False

      else:
        if ot1 not in ["INCOMING BATTLE", "YOU WIN", "YOU LOSE"]:
          display("PRESS A TO", "START A BATTLE")
          readNumpad()
          if inp != "":
            if inp[-1] == "A":
              sendBattle()
          else:
            tx = processIRRemote()
            if tx == "Source":
              createBattle()

thread = threading.Thread(target=main)
thread.start()

def displayWL(message):
  global win
  win = True
  display(message)
  time.sleep(5)
  checkInBattle()
  return

while True:
  with socketio.SimpleClient() as sio:
    sio.connect(backend_uri)
    message = sio.receive()
    if inBattle:
      if (message[0] == uid):
        refreshMagicianState()
      elif (message[0] == uid + "win"):
        thread = threading.Thread(target=lambda: displayWL("YOU WIN!"))
        thread.start()
      elif (len(message) > 1):
        thread = threading.Thread(target=lambda: displayWL("YOU WIN!"))
        thread.start()
    else:
      if (message[0] == uid):
        checkInBattle()