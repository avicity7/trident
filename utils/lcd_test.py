import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

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

while True:
    lcd.cursor_position(0, 0)# coloumn,row
    lcd.message = "No active battle"
    lcd.cursor_position(0, 1)
    lcd.message = "Searching"
    time.sleep(10)
    lcd.clear()
    time.sleep(10)
