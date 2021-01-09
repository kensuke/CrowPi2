#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author : original author Elecrow and other contributors

# https://qiita.com/Kobayashi2019/items/03e31ee50b924f428e71
# don't create __pycache__
import sys
sys.dont_write_bytecode = True

################################################################################
# DATA Definition                                                              #
################################################################################
gpio_pins = [
    # PHYSICAL Port No., GPIO No., BCM No.
    #PHY GP  BCM  DESC          PHY GP  BCM  DESC       # Always ON
    [ 1, -1, -1, '3V3'],       [ 2, -1, -1, '5V'],      # * *
    [ 3, -1,  2, 'SDA1'],      [ 4, -1, -1, '5V'],      #   *
    [ 5, -1,  3, 'SCL1'],      [ 6, -1, -1, 'GND'],     # I2C
    [ 7, -1,  4, '1Wire'],     [ 8, -1, 14, 'TxD'],
    [ 9, -1, -1, 'GND'],       [10, -1, 15, 'RxD'],
    [11,  0, 17, 'Touch'],     [12,  1, 18, 'Buzzer'],
    [13,  2, 27, 'Vibration'], [14, -1, -1, 'GND'],
    [15,  3, 22, 'Tilt'],      [16,  4, 23, 'Motion'],  # * *blink
    [17, -1, -1, '3V3'],       [18,  5, 24, 'Sound'],   # *
    [19, -1, 10, 'MOSI'],      [20, -1, -1, 'GND'],
    [21, -1,  9, 'MISO'],      [22,  6, 25, 'Servo-M'],
    [23, -1, 11, 'SCLK'],      [24, -1,  8, 'CE0'],
    [25, -1, -1, 'GND'],       [26, -1,  7, 'CE1'],
    [27, -1,  0, 'SDA0'],      [28, -1,  1, 'SCL0'],    # *
    [29, 21,  5, 'Step-M-1'],  [30, -1, -1, 'GND'],
    [31, 22,  6, 'Step-M-2'],  [32, 26, 12, 'RGB Matrix?'],
    [33, 23, 13, 'Step-M-3'],  [34, -1, -1, 'GND'],
    [35, 24, 19, 'Step-M-4'],  [36, 27, 16, 'Ultrasonic-TRIG'],
    [37, 25, 26, 'Uls-ECHO'],  [38, 28, 20, 'IR'],
    [39, -1, -1, 'GND'],       [40, 29, 21, 'Relay'],
]

################################################################################
# INPUT                                                                        #
################################################################################

######################################################################
# Joystick
import spidev
import time
class Joystick():

    def __init__(self):
        print('/usr/share/code/project/Memory/Memory.py')
        print('Press CTRL+C to exit')

        self.x_channel = 1
        self.y_channel = 0

        self.delay = 0.05
 
        # Open SPI bus
        self.spi = spidev.SpiDev()
        self.spi.open(0,1)
        self.spi.max_speed_hz=1000000

    # Function to read SPI data from MCP3008 chip
    # Channel must be an integer 0-7
    def ReadChannel(self, channel):
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

    def sprite(self):
        # Read the  data
        x_value = self.ReadChannel(self.x_channel)
        y_value = self.ReadChannel(self.y_channel)
        print("(x, y) = ("+str(x_value)+", "+str(y_value)+")")
        if x_value > 650:
            print("Left")
        if x_value < 400:
            print("Right")
        if y_value > 650:
            print("Up")
        if y_value < 400:
            print("Down")

        # Wait before repeating loop
        time.sleep(self.delay)

    def main(self):
        try:
            while True:
                self.sprite()
        except KeyboardInterrupt:
            pass

######################################################################
# matrix button
import spidev
import time
class ButtonMatrix():

    def __init__(self):
        print('/usr/share/code/project/Calculator/Calculator.py')
        print('Author : original author stenobot')
        print('Original Author Github: https://github.com/stenobot/SoundMatrixPi')
        print('Press CTRL+C to exit')

        # Open SPI bus
        self.spi = spidev.SpiDev()
        self.spi.open(0,1)
        self.spi.max_speed_hz=1000000

        # Define key channels
        self.key_channel = 4
        self.delay = 0.1

        self.adc_key_val = [30,90,160,230,280,330,400,470,530,590,650,720,780,840,890,960]
        self.key = -1
        self.oldkey = -1
        self.num_keys = 16

        self.indexes = {
            12:7, 13:8,  14:9,  15:'x',
             8:4,  9:5,  10:6,  11:'/',
             4:1,  5:2,   6:3,   7:'+',
             0:0,  1:'#', 2:'=', 3:'-'
        }

    def ReadChannel(self,channel):
        # Function to read SPI data from MCP3008 chip
        # Channel must be an integer 0-7
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data
    
    def GetAdcValue(self):
        adc_key_value = self.ReadChannel(self.key_channel)
        return adc_key_value

    def GetKeyNum(self,adc_key_value):
        for num in range(0,16):
            if adc_key_value < self.adc_key_val[num]:
                return num
        if adc_key_value >= self.num_keys:
            num = -1
            return num

    def activateButton(self, btnIndex):
        # get the index from SPI
        btnIndex = int(btnIndex)
        # correct the index to better format
        btnIndex = self.indexes[btnIndex]
        print("button %s pressed" % btnIndex)
        # prevent button presses too close together
        time.sleep(.3)

    def main(self):
        try:
            while True:
                # get buttons press from SPI
                self.adc_key_value = self.GetAdcValue()
                self.key = self.GetKeyNum(self.adc_key_value)
                if self.key != self.oldkey:
                    time.sleep(0.05)
                    self.adc_key_value = self.GetAdcValue()
                    self.key = self.GetKeyNum(self.adc_key_value)
                    if self.key != self.oldkey:
                        self.oldkey = self.key
                        if self.key >= 0:
                            # button pressed, activate it
                            self.activateButton(self.key)
                time.sleep(self.delay)
        except KeyboardInterrupt:
            pass

######################################################################
# Touch Sensor
import RPi.GPIO as GPIO
import time
class TouchSensor():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/touch.py')
        print('Touch Button')
        print('Press CTRL+C to exit')

        # define touch pin
        touch_pin = 17
        # set board mode to GPIO.BCM
        GPIO.setmode(GPIO.BCM)
        # set GPIO pin to INPUT
        GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        try:
            while True:
               # check if touch detected
               if(GPIO.input(touch_pin)):
                   print('Touch Detected')
               time.sleep(0.1)
        except KeyboardInterrupt:
            # CTRL+C detected, cleaning and quitting the script
            GPIO.cleanup()

######################################################################
# RFID Reader
import RPi.GPIO as GPIO
import time
class RFIDReader():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/RFID/Read.py & MFRC522.py')
        print('Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>')


        # https://qiita.com/yuukiclass/items/88e9ac6c5a3b5ab56cc4
        try:
            import MFRC522
        except Exception as e:
            print(e)
            url = 'https://raw.githubusercontent.com/Elecrow-RD/CrowPi/master/Examples/RFID/MFRC522.py'
            print('downloading MFRC522.py from ' + url)
            import urllib.request # for python3
            urllib.request.urlretrieve(url, 'MFRC522.py')
            time.sleep(0.5) # a few rest

            try:
                import MFRC522
            except Exception as e:
                print(e)
                return

        try:
        # Incase user wants to terminate, this function is exactly for that reason.
#            import signal
#            signal.signal(signal.SIGINT, end_read)
            # create the reader object
            MIFAREReader = MFRC522.MFRC522()

            # Welcome greeting
            print("Welcome to MFRC522 RFID Read example")
            print("Press CTRL+C anytime to quit.")

            # The function will continue running to detect untill user said otherwise
            while True: #continue_reading:
                # detect touch of the card, get status and tag type
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                # check if card detected or not
                if status == MIFAREReader.MI_OK:
                    print("Card detected")

                # Get the RFID card uid and status
                (status,uid) = MIFAREReader.MFRC522_Anticoll()

                # If status is alright, continue to the next stage
                if status == MIFAREReader.MI_OK:
                    # Print UID
                    print("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
                    # standard key for rfid tags
                    key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                    # Select the scanned tag
                    MIFAREReader.MFRC522_SelectTag(uid)
                    # authenticate
                    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
                    # check if authenticated successfully, read the data
                    if status == MIFAREReader.MI_OK:
                        MIFAREReader.MFRC522_Read(8)
                        MIFAREReader.MFRC522_StopCrypto1()
                    else:
                        print("Authentication error")
        except KeyboardInterrupt:
            print("Ctrl+C captured, ending read.")
            GPIO.cleanup()

################################################################################
# OUTPUT                                                                       #
################################################################################

######################################################################
# 4 digit segment
import datetime
from Adafruit_LED_Backpack import SevenSegment
import time
class FourDigitSegment():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/segment.py')

        # ===========================================================================
        # Clock Example
        # ===========================================================================
        segment = SevenSegment.SevenSegment(address=0x70)

        # Continually update the time on a 4 char, 7-segment display
        try:
            # Initialize the display. Must be called once before using the display.
            segment.begin()
            print('Press CTRL+C to exit')

            for i in range(10):
                segment.set_digit(0, i)
                segment.set_digit(1, (i+1)%10)
                segment.set_digit(2, (i+2)%10)
                segment.set_digit(3, (i+3)%10)
                segment.write_display()
                time.sleep(0.2)

            while(True):
                now = datetime.datetime.now()
                hour = now.hour
                minute = now.minute
                second = now.second

                segment.clear()
                # Set hours
                segment.set_digit(0, int(hour / 10))     # Tens
                segment.set_digit(1, hour % 10)          # Ones
                # Set minutes
                segment.set_digit(2, int(minute / 10))   # Tens
                segment.set_digit(3, minute % 10)        # Ones
                # Toggle colon
                segment.set_colon(second % 2)              # Toggle colon at 1Hz

                # Write the display buffer to the hardware.  This must be called to
                # update the actual display LEDs.
                segment.write_display()

                # Wait a quarter second (less than 1 second to prevent colon blinking getting$
                time.sleep(0.25)
        except KeyboardInterrupt:
            segment.clear()
            segment.write_display()

######################################################################
# GPIO LED Blink
import RPi.GPIO as GPIO
import time
class GPIOLed():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/blinking_led.py')
        print('Press CTRL+C to exit')

        # define LED pin
        led_pin = 26
        # set GPIO mode to GPIO.BCM
        GPIO.setmode(GPIO.BCM)
        # set pin as OUTPUT
        GPIO.setup(led_pin, GPIO.OUT)

        try:
            while True:
                # turn on LED
                GPIO.output(led_pin, GPIO.HIGH)
                # Wait half a second
                time.sleep(0.2)
                # turn off LED
                GPIO.output(led_pin, GPIO.LOW)
                # Wait half a second
                time.sleep(0.2)
        except KeyboardInterrupt:
            # CTRL+C detected, cleaning and quitting the script
            GPIO.cleanup()

######################################################################
# (GPIO LED Blink)
import RPi.GPIO as GPIO
import time
class GPIOLed_DONOT_USE():

    def __init__(self):
        print('BUG: i2c timeout after this test. AT YOUR OWN RISK!')
        print('Press CTRL+C to exit')

#        GPIO.setmode(GPIO.BOARD)

        for pins in range(len(gpio_pins)):
            pin = gpio_pins[pins]
            # TODO: more need skip pins!
            if pin[3] == '3V3' or pin[3] == '5V' or pin[3] == 'GND' or pin[3] == 'SDA0' or pin[3] == 'SCL0':
                pass
            else:
                GPIO.setup(pin[0], GPIO.OUT)

        try:
            while True:
                for pins in range(len(gpio_pins)/2):
                    pin_o = gpio_pins[pins * 2]     # PYH odd  pin 1,3,5...
                    pin_e = gpio_pins[pins * 2 + 1] # PYH even pin 2,4,6...

                    if pin_o[3] == '3V3' or pin_o[3] == '5V' or pin_o[3] == 'GND' or pin_o[3] == 'SDA0':
                        pin_o = -1
                    if pin_e[3] == '3V3' or pin_e[3] == '5V' or pin_e[3] == 'GND' or pin_e[3] == 'SCL0':
                        pin_e = -1

                    if pin_o == -1 and pin_e == -1:
                        continue

                    # turn on LED
                    if pin_o != -1:
                        GPIO.output(pin_o[0], GPIO.HIGH)
                    if pin_e != -1:
                        GPIO.output(pin_e[0], GPIO.HIGH)
                    # Wait half a second
                    time.sleep(0.2)

                    # turn off LED
                    if pin_o != -1:
                        GPIO.output(pin_o[0], GPIO.LOW)
                    if pin_e != -1:
                        GPIO.output(pin_e[0], GPIO.LOW)
                    # Wait half a second
                    time.sleep(0.2)

        except KeyboardInterrupt:
            # CTRL+C detected, cleaning and quitting the script
            GPIO.cleanup()

######################################################################
# LCD
# Example using a character LCD backpack.
import Adafruit_CharLCD as LCD
import time
class LCD1602():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/lcd.py')
        print('Press CTRL+C to exit')

        # Define LCD column and row size for 16x2 LCD.
        lcd_columns = 16
        lcd_rows    = 2

        # Initialize the LCD using the pins
        lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

        try:
            # Turn backlight on
            lcd.set_backlight(0)

            # Print a two line message
            for i in range(5):
                lcd.message('Hello\nworld! in '+str(5-i)+' secs')

                # Wait 1 seconds
                time.sleep(1.0)

            # Demo showing the cursor.
            lcd.clear()
            lcd.show_cursor(True)
            lcd.message('Show cursor')

            time.sleep(5.0)

            # Demo showing the blinking cursor.
            lcd.clear()
            lcd.blink(True)
            lcd.message('Blink cursor')

            time.sleep(5.0)

            # Stop blinking and showing cursor.
            lcd.show_cursor(False)
            lcd.blink(False)

            # Demo scrolling message right/left.
            lcd.clear()
            message = 'Scroll'
            lcd.message(message)
            for i in range(lcd_columns-len(message)):
                time.sleep(0.5)
                lcd.move_right()
            for i in range(lcd_columns-len(message)):
                time.sleep(0.5)
                lcd.move_left()

            # Demo turning backlight off and on.
            lcd.clear()
            lcd.message('Flash backlight\nin 5 seconds...')
            time.sleep(5.0)

            # Turn backlight off.
            lcd.set_backlight(1)
            time.sleep(2.0)

            # Change message.
            lcd.clear()
            lcd.message('Goodbye!')

            # Turn backlight on.
            lcd.set_backlight(0)

            # Turn backlight off.
            time.sleep(2.0)
            lcd.clear()
            lcd.set_backlight(1)

        except KeyboardInterrupt:
            # Turn the screen off
            lcd.clear()
            lcd.set_backlight(1)

######################################################################
# LED matrix
from rpi_ws281x import PixelStrip, Color
import random
import time
class RGBMatrix1:

    def __init__(self):
        print('/usr/share/code/project/Tilt_reminder/Tilt_reminder.py')
        print('Required root privileges!')
        print('Press CTRL+C to exit')

        # LED strip configuration:
        LED_COUNT = 64        # Number of LED pixels.
        LED_PIN = 12          # GPIO pin connected to the pixels (18 uses $
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800$
        LED_DMA = 10          # DMA channel to use for generating signal ($
        LED_BRIGHTNESS = 10   # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False    # True to invert the signal (when using NPN $
        LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        # TODO: root
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

            #  0  1  2  3  4  5  6  7
            #  8  9 10 11 12 13 14 15
            # 16 17 18 19 20 21 22 23
            # 24 25 26 27 28 29 30 31
            # 32 33 34 35 36 37 38 39
            # 40 41 42 43 44 45 46 47
            # 48 49 50 51 52 53 54 55
            # 56 57 58 59 60 61 62 63
    def main(self):
        numbers = [
            [0, 1, 2, 3, 4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8], # 0
            [3, 11, 19, 27, 35, 43, 51, 59], # 1
            [9, 2, 3, 4, 13, 21, 28, 28, 34, 41, 49, 57, 58, 59, 60, 61],     # 2
            [2, 3, 4, 13, 21, 28, 27, 26, 25, 37, 45, 53, 60, 59, 58, 57],    # 3
            [1, 9, 17, 25, 33, 41, 42, 43, 44, 45, 46, 47, 28, 36, 52, 60],   # 4
            [1, 9, 17, 25, 26, 27, 28, 29, 38, 46, 54, 61, 60, 59, 58, 57, 2, 3, 4, 5], # 5
            [6, 5, 4, 3, 2, 1, 9, 17, 25, 33, 41, 49, 57, 58, 59, 60, 61, 62, 54, 46, 38, 37, 36, 35, 34], # 6
            [1, 2, 3, 4, 5, 6, 7, 15, 22, 29, 36, 44, 52, 60],                # 7
            [4, 3, 2, 9, 18, 27, 36, 45, 53, 60, 59, 58, 49, 41, 34, 20, 13], # 8
            [7, 6, 5, 4, 3, 2, 1, 9, 17, 25, 33, 34, 35, 36, 37, 38, 39, 31, 23, 15, 47, 55, 63, 62, 61, 60, 59, 58, 57] # 9
        ]

        try:
            # full pixles
            self.colorWipe(Color(0,0,0), 10)
            for cell in range(8*8):
                r, g, b = random.randint(10, 250), random.randint(10, 250), random.randint(10, 250)
                self.strip.setPixelColor(cell, Color(r, g, b))
            self.strip.show()
            time.sleep(0.1)

            # numbers 0-9
            self.colorWipe(Color(0,0,0), 10)
            for num in numbers:
                r, g, b = random.randint(10, 250), random.randint(10, 250), random.randint(10, 250)
                for cell in num:
                    self.strip.setPixelColor(cell, Color(r, g, b))
                self.strip.show()
                time.sleep(0.1)
                for cell in num:
                    self.strip.setPixelColor(cell, Color(0,0,0))
                self.strip.show()
            time.sleep(0.1)

            while True:
                num = numbers[random.randint(0, len(numbers)-1)]
                r, g, b = random.randint(10, 250), random.randint(10, 250), random.randint(10, 250)
                for cell in num:
                    self.strip.setPixelColor(cell, Color(r, g, b))
                self.strip.show()
                time.sleep(0.1)
                for cell in num:
                    self.strip.setPixelColor(cell, Color(0,0,0))
                self.strip.show()
        except KeyboardInterrupt:
            self.colorWipe(Color(0,0,0), 10)

################################################################################
# Sensor                                                                       #
################################################################################

######################################################################
# DHT11 temperature
import Adafruit_DHT
class DHT():
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/dh11.py')
        print('Mesuaring temperature & humidity...')
        print('Press CTRL+C to exit')

        # set type of the sensor
        sensor = 11
        # set pin number
        pin = 4

        try:
            while True:
                # Try to grab a sensor reading.  Use the read_retry method which will retry up
                # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
                humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

                # Un-comment the line below to convert the temperature to Fahrenheit.
                fahrenheit = temperature * 9/5.0 + 32

                # Note that sometimes you won't get a reading and
                # the results will be null (because Linux can't
                # guarantee the timing of calls to read the sensor).
                # If this happens try again!
                if humidity is not None and temperature is not None:
                    print('Temp={0:0.1f}C, {1:0.1f}F,  Humidity={2:0.1f}%'.format(temperature, fahrenheit, humidity))
                else:
                    print('Failed to get reading. Try again!')
        except KeyboardInterrupt:
            pass

######################################################################
# Tilt
import RPi.GPIO as GPIO
import time
class Tilt():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/tilt.py')
        print('Press CTRL+C to exit')

        # define tilt pin
        tilt_pin = 22
        # set GPIO mode to GPIO.BCM
        GPIO.setmode(GPIO.BCM)
        # set puin as INPUT
        GPIO.setup(tilt_pin, GPIO.IN)

        try:
            while True:
                # positive is tilt to left negative is tilt to right
                tilt = GPIO.input(tilt_pin)
                if tilt:
                    print("[<-]("+str(tilt)+") Left Tilt")
                else:
                    print("[->]("+str(tilt)+") Right Tilt")
                time.sleep(1)
        except KeyboardInterrupt:
            # CTRL+C detected, cleaning and quitting the script
            GPIO.cleanup()

######################################################################
# PIR MOtion Sensor
import RPi.GPIO as GPIO
import time
class Motion():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/motion.py')
        print('Press CTRL+C to exit')

        # define motion pin
        motion_pin = 23
        # set GPIO as GPIO.BCM
        GPIO.setmode(GPIO.BCM)
        # set pin mode as INPUT
        GPIO.setup(motion_pin, GPIO.IN)

        try:
            while True:
                mot = GPIO.input(motion_pin)
                if(mot):
                    print("("+str(mot)+") Motion detected!")
                else:
                    print("("+str(mot)+") Nothing moves ...")
                time.sleep(0.1)
        except KeyboardInterrupt:
            GPIO.cleanup()

######################################################################
# Sound Detect Sensor
import RPi.GPIO as GPIO
import time
class Sound():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/sound.py')
        print('Press CTRL+C to exit')

        # define sound pin
        sound_pin = 24
        # set GPIO mode to GPIO.BOARD
        GPIO.setmode(GPIO.BCM)
        # setup pin as INPUT
        GPIO.setup(sound_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        try:
            while True:
                # check if sound detected or not
                if(GPIO.input(sound_pin)==GPIO.LOW):
                    print('Sound Detected')
                else:
                    print('Sound of Silence')
                time.sleep(0.1)
        except KeyboardInterrupt:
            # CTRL+C detected, cleaning and quitting the script
            GPIO.cleanup()

######################################################################
# Light Sensor
import RPi.GPIO as GPIO
import smbus
import time
class LightSensor():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/light_sensor.py')
        print('Author: Matt Hawkins')
        print('Author\'s Git: https://bitbucket.org/MattHawkinsUK/')
        print('Author\'s website: https://www.raspberrypi-spy.co.uk')
        print('Press CTRL+C to exit')

        # Find the right revision for bus driver
        if(GPIO.RPI_REVISION == 1):
            self.bus = smbus.SMBus(0)
        else:
            self.bus = smbus.SMBus(1)

        # Define some constants from the datasheet
        self.DEVICE = 0x5c # Default device I2C address

        self.POWER_DOWN = 0x00 # No active state
        self.POWER_ON = 0x01 # Power on
        self.RESET = 0x07 # Reset data register value

        # Start measurement at 4lx resolution. Time typically 16ms.
        self.CONTINUOUS_LOW_RES_MODE = 0x13
        # Start measurement at 1lx resolution. Time typically 120ms
        self.CONTINUOUS_HIGH_RES_MODE_1 = 0x10
        # Start measurement at 0.5lx resolution. Time typically 120ms
        self.CONTINUOUS_HIGH_RES_MODE_2 = 0x11
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_HIGH_RES_MODE_1 = 0x20
        # Start measurement at 0.5lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_HIGH_RES_MODE_2 = 0x21
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_LOW_RES_MODE = 0x23

    def convertToNumber(self, data):
        # Simple function to convert 2 bytes of data
        # into a decimal number
        return ((data[1] + (256 * data[0])) / 1.2)

    def readLight(self):
        data = self.bus.read_i2c_block_data(self.DEVICE,self.ONE_TIME_HIGH_RES_MODE_1)
        return self.convertToNumber(data)

    def main(self):
        try:
            while True:
                print("Light Level : " + str(self.readLight()) + " lx")
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass

######################################################################
# Ultrasonic Sensor
import RPi.GPIO as GPIO
import time
class Ultrasonic():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/distance.py')
        print('Author : www.modmypi.com')
        print('Link: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi')
        print('Press CTRL+C to exit')

        GPIO.setmode(GPIO.BCM)

        TRIG = 16
        ECHO = 26 # CrowPi1 12

        print("Distance Measurement In Progress")

        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)

        try:
            while True:
                GPIO.output(TRIG, False)
                print("Waiting For Sensor To Settle in 2 seconds")
                time.sleep(2)

                GPIO.output(TRIG, True)
                time.sleep(0.00001)
                GPIO.output(TRIG, False)

                while GPIO.input(ECHO)==0:
                    pulse_start = time.time()

                while GPIO.input(ECHO)==1:
                    pulse_end = time.time()

                pulse_duration = pulse_end - pulse_start

                distance = pulse_duration * 17150
                distance = round(distance, 2)
                print("Distance: %scm" % distance)
        except KeyboardInterrupt:
            GPIO.cleanup()

################################################################################
# Hardware                                                                     #
################################################################################

######################################################################
# Relay
import RPi.GPIO as GPIO
import time
class Relay():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/relay.py')

        # define relay pin
        relay_pin = 21
        # set GPIO mode as GPIO.BCM
        GPIO.setmode(GPIO.BCM)
        # setup relay pin as OUTPUT
        GPIO.setup(relay_pin, GPIO.OUT)

        # Open Relay
        GPIO.output(relay_pin, GPIO.LOW)
        # Wait half a second
        time.sleep(0.5)

        # Close Relay
        GPIO.output(relay_pin, GPIO.HIGH)
        # Wait half a second
        time.sleep(0.5)
        # Close Relay
        GPIO.output(relay_pin, GPIO.LOW)
        GPIO.cleanup()


######################################################################
# Switch
import RPi.GPIO as GPIO
import time
class Switch():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/touch.py')
        print('Switch On or Off with Touch Button')
        print('Press CTRL+C to exit')

        # define touch pin
        touch_pin = 17
        # set board mode to GPIO.BCM
        GPIO.setmode(GPIO.BCM)
        # set GPIO pin to INPUT
        GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        try:
            while True:
               # check if touch detected
               if(GPIO.input(touch_pin)):
                   print('Touch Detected') # TODO: always detedted when switch off ;-)
               time.sleep(0.1)
        except KeyboardInterrupt:
            # CTRL+C detected, cleaning and quitting the script
            GPIO.cleanup()

######################################################################
# Buzzer
import RPi.GPIO as GPIO
import time
class Buzzer():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/buzzer.py')
        print('beep 1 second, stop 3 seconds')
        print('Press CTRL+C to exit')

        buzzer_pin = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer_pin, GPIO.OUT)

        try:
            while True:
                # Make buzzer sound
                GPIO.output(buzzer_pin, GPIO.HIGH)
                time.sleep(1)

                # Stop buzzer sound
                GPIO.output(buzzer_pin, GPIO.LOW)
                time.sleep(3)
        except KeyboardInterrupt:
            GPIO.cleanup()

######################################################################
# Touch And Buzzer
import RPi.GPIO as GPIO
class TouchButtonAndBuzzer():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/button_buzzer.py')
        print('Press CTRL+C to exit')

        # configure both button and buzzer pins
        button_pin = 17 # CrowPi1 26
        buzzer_pin = 18
        # set board mode to GPIO.BCM
        GPIO.setmode(GPIO.BCM)
        # setup button pin asBu input and buzzer pin as output
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(buzzer_pin, GPIO.OUT)

        try:
            while True:
            # check if button pressed
                if(GPIO.input(button_pin) == 1):
                    # set buzzer on
                    GPIO.output(buzzer_pin, GPIO.HIGH)
                else:
                    # it's not pressed, set button off
                    GPIO.output(buzzer_pin, GPIO.LOW)
        except KeyboardInterrupt:
            GPIO.cleanup()

######################################################################
# Vibration
import RPi.GPIO as GPIO
import time
class Vibration():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/vibration.py')
        print('moving 1 second, stop 3 seconds')
        print('Press CTRL+C to exit')

        # define vibration pin
        vibration_pin = 27
        # Set board mode to GPIO.BCM
        GPIO.setmode(GPIO.BCM)
        # Setup vibration pin to OUTPUT
        GPIO.setup(vibration_pin, GPIO.OUT)

        try:
            while True:
                # turn on vibration
                GPIO.output(vibration_pin, GPIO.HIGH)
                # wait a second
                time.sleep(1)

                # turn off vibration
                GPIO.output(vibration_pin, GPIO.LOW)
                # wait 3 seconds
                time.sleep(3)
        except KeyboardInterrupt:
            # cleaup GPIO
            GPIO.cleanup()

################################################################################
# Interface                                                                    #
################################################################################

######################################################################
# IR
import RPi.GPIO as GPIO
import time
class IR:

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/IR_New.py')
        print('Press CTRL+C to exit')

        # Define IR pin
        self.PIN = 20
        GPIO.setmode(GPIO.BCM)
        # setup IR pin as input
        GPIO.setup(self.PIN, GPIO.IN, GPIO.PUD_UP)

        print("irm test start...")

        self.indexes = {
            0x45:'CH-',  0x46:'CH',   0x47:'CH+',
            0x44:'PREV', 0x40:'NEXT', 0x43:'PLAY',
            0x07:'VOL-', 0x15:'VOL+', 0x09:'EQ',
            0x16:'0',    0x19:'100+', 0x0d:'200+',
            0x0c:'1',    0x18:'2',    0x5e:'3',
            0x08:'4',    0x1c:'5',    0x5a:'6',
            0x42:'7',    0x52:'8',    0x4a:'9'
        }

    def decode(self, key_val):
        if not key_val in self.indexes:
            return 'Unknown'
        return self.indexes[key_val]

    def main(self):
        try:
            while True:
                if GPIO.input(self.PIN) != 0:
                    continue
                
                count = 0
                while GPIO.input(self.PIN) == 0 and count < 200:
                    count += 1
                    time.sleep(0.00006)

                count = 0
                while GPIO.input(self.PIN) == 1 and count < 80:
                    count += 1
                    time.sleep(0.00006)

                idx = 0
                cnt = 0
                data = [0,0,0,0]
                for i in range(0,32):
                    count = 0
                    while GPIO.input(self.PIN) == 0 and count < 15:
                        count += 1
                        time.sleep(0.00006)

                    count = 0
                    while GPIO.input(self.PIN) == 1 and count < 40:
                        count += 1
                        time.sleep(0.00006)

                    if count > 8:
                        data[idx] |= 1<<cnt
                    if cnt == 7:
                        cnt = 0
                        idx += 1
                    else:
                        cnt += 1

                if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:
                    print("Get the key[0x%02x][%s]" % (data[2], self.decode(data[2])))
        except KeyboardInterrupt:
            GPIO.cleanup()

######################################################################
# Crowtail - Moisture Sensor
import RPi.GPIO as GPIO
import time
class MoistureSensor:

    def __init__(self):
        print('/home/pi/user/<User Name>/python/plant_water_monitoring.py')
        print('Press CTRL+C to exit')

        #GPIO SETUP
        soil_pin = 19 # I2C port=3
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(soil_pin, GPIO.IN)

        try:
            while True:
                mois = GPIO.input(soil_pin)
                msg = 'filled moisture' if mois == 1 else 'thirsty'
                print('Moisture Value[' +str(mois)+ '] ' + msg)
                # wait 0.1 seconds before try again
                time.sleep(0.1)
        except KeyboardInterrupt:
            GPIO.cleanup()

######################################################################
# Servo Motor
import RPi.GPIO as GPIO
import time
class sg90:

    def __init__( self, direction = 0):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/servo.py')
        print('Author : Original author WindVoiceVox')
        print('Original Author Github: https://github.com/WindVoiceVox/Raspi_SG90')
        print('Press CTRL+C to exit')

        self.pin = 19 # CrowPi1 25
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( self.pin, GPIO.OUT )
        self.direction = int( direction )
        self.servo = GPIO.PWM( self.pin, 50 )
        self.servo.start(0.0)

    def cleanup( self ):
        self.servo.ChangeDutyCycle(self._henkan(0))
        time.sleep(0.3)
        self.servo.stop()
        GPIO.cleanup()

    def currentdirection( self ):
       return self.direction

    def _henkan( self, value ):
       return 0.05 * value + 7.0

    def setdirection( self, direction, speed ):
        for d in range( self.direction, direction, int(speed) ):
            self.servo.ChangeDutyCycle( self._henkan( d ) )
            self.direction = d
            time.sleep(0.1)
        self.servo.ChangeDutyCycle( self._henkan( direction ) )
        self.direction = direction

    def main(self):
        try:
            while True:
                print("Turn left ...")
                self.setdirection( 100, 80 )
                time.sleep(0.5)
                print("Turn right ...")
                self.setdirection( -100, 80 )
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.cleanup()

######################################################################
# Servo Like Step Motor
import math
import RPi.GPIO as GPIO
import time
class ServoMotor_LikeStep():

    def __init__(self):
        print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/stepmotor.py')
        print('Author : Original author ludwigschuster')
        print('Original Author Github: https://github.com/ludwigschuster/RasPi-GPIO-Stepmotor')
        print('Press CTRL+C to exit')

		# set GPIO mode
        GPIO.setmode(GPIO.BCM)
        # These are the pins which will be used on the Raspberry Pi
        self.pin_A = 5
        self.pin_B = 6
        self.pin_C = 13
        self.pin_D = 19
        self.interval = 0.010

        # Declare pins as output
        GPIO.setup(self.pin_A,GPIO.OUT)
        GPIO.setup(self.pin_B,GPIO.OUT)
        GPIO.setup(self.pin_C,GPIO.OUT)
        GPIO.setup(self.pin_D,GPIO.OUT)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)
        GPIO.output(self.pin_D, False)

    def Step1(self):
        GPIO.output(self.pin_D, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)

    def Step2(self):
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_C, False)

    def Step3(self):
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_C, False)

    def Step4(self):
        GPIO.output(self.pin_B, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)

    def Step5(self):
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)

    def Step6(self):
        GPIO.output(self.pin_A, True)
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)

    def Step7(self):
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)

    def Step8(self):
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_A, False)

    def turn(self,count):
        for i in range (int(count)):
            self.Step1()
            self.Step2()
            self.Step3()
            self.Step4()
            self.Step5()
            self.Step6()
            self.Step7()
            self.Step8()

    def close(self):
        # cleanup the GPIO pin use
        GPIO.cleanup()

    def turnSteps(self, count):
        # Turn n steps
        # (supply with number of steps to turn)
        for i in range (count):
            self.turn(1)

    def turnDegrees(self, count):
        # Turn n degrees (small values can lead to inaccuracy)
        # (supply with degrees to turn)
        self.turn(round(count*512/360,0))

    def turnDistance(self, dist, rad):
        # Turn for translation of wheels or coil (inaccuracies involved e.g. due to thickness of rope)
        # (supply with distance to move and radius in same metric)
        self.turn(round(512*dist/(2*math.pi*rad),0))

    def main(self):
        print("moving started")

        print("One Step")
        self.turnSteps(1)
        time.sleep(3) # 0.5 # TODO: asynchronous

        print("3 Steps") # 20
        self.turnSteps(3) # 20
        time.sleep(3) # 0.5

        print("quarter turn")
        self.turnDegrees(90)

        print("moving stopped")
        self.close()

######################################################################
# Step Motor
import math
import RPi.GPIO as GPIO
import time
class StepMotor():

    def __init__(self):
        print('/usr/share/code/project/Lucky_turntable')
        print('Press CTRL+C to exit')

        # set GPIO BCM mode
        GPIO.setmode(GPIO.BCM)

        # These are the pins which will be used on the Raspberry Pi
        self.pin_A = 5
        self.pin_B = 6
        self.pin_C = 13
        self.pin_D = 25
        self.interval = 0.0011

        # Declare pins as output
        GPIO.setup(self.pin_A,GPIO.OUT)
        GPIO.setup(self.pin_B,GPIO.OUT)
        GPIO.setup(self.pin_C,GPIO.OUT)
        GPIO.setup(self.pin_D,GPIO.OUT)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)
        GPIO.output(self.pin_D, False)

    def Step1(self):
        GPIO.output(self.pin_D, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)

    def Step2(self):
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_C, False)

    def Step3(self):
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_C, False)

    def Step4(self):
        GPIO.output(self.pin_B, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)

    def Step5(self):
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)

    def Step6(self):
        GPIO.output(self.pin_A, True)
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)

    def Step7(self):
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)

    def Step8(self):
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_A, False)

    def turn(self,count):
        for i in range (int(count)):
            self.Step1()
            self.Step2()
            self.Step3()
            self.Step4()
            self.Step5()
            self.Step6()
            self.Step7()
            self.Step8()

    def turnSteps(self, count):
        # Turn n steps
        # (supply with number of steps to turn)
        for i in range (count):
            self.turn(1)

    def turnDegrees(self, count):
        # Turn n degrees (small values can lead to inaccuracy)
        # (supply with degrees to turn)
        self.turn(round(count*512/360,0))

    def turnDistance(self, dist, rad):
        # Turn for translation of wheels or coil (inaccuracies involved e.g. due to thickness of rope)
        # (supply with distance to move and radius in same metric)
        self.turn(round(512*dist/(2*math.pi*rad),0))

    def main(self):
        print("moving started")
        print("360 turn")
        for i in range(1): # 7
            self.turnDegrees(360)
        print("moving stopped")
        GPIO.cleanup()

################################################################################
# main menu                                                                    #
################################################################################

# menu item definition
# sys, GPIO, BCM, Category, H/W, Class Name
menu_items = [
# FIXME: How to test?
    [ 4, -1, -1, 'Disp', 'Screen driver / If you seen this, screen is working (^ ^)/'],
    [ 5, -1, -1, 'Other', 'Cooling fan / How to control fan on software?'],
    [ 7, -1, -1, 'I/F', 'GPIO export'],
    [10, -1, -1, 'I/F', 'Breadboard'],
    [16, -1,  3, 'I/F', 'I/O/ADC/I2C/UART expantion interface'],
# TODO: How to get current setting values?
    [21, -1, -1, 'Other', 'PIR sensitivity adjustment'],
    [23, -1, -1, 'Other', 'Sound sensor sensitivity adjustment'],
    [28, -1, -1, 'Other', 'LCD1602 brightness adjustment'],

    [ 1, -1, -1, 'Input', 'Joystick', 'Joystick'],
    [19, -1, -1, 'Input', '4x4 button matrix', 'ButtonMatrix'],
    [24,  0, 17, 'Input', 'Touch sensor', 'TouchSensor'],
    [26, -1, -1, 'Input', 'RC522 RFID induction module / Required MFRC522.py', 'RFIDReader'],

    [ 2, -1, -1, 'Disp', '4 Digits Segment LED', 'FourDigitSegment'],
    [ 8, 25, 26, 'Disp', 'GPIO indicate LED / only 26pin', 'GPIOLed'],
#    [88, 25, 26, 'Disp', 'GPIO indicate LED', 'GPIOLed_DONOT_USE'], # for advanced users
    [12, -1, -1, 'Disp', 'LCD1602', 'LCD1602'],
    [25, -1, -1, 'Disp', '8x8 RGB matrix / ** Required root privileges! **', 'RGBMatrix1'],

    [ 9, -1, -1, 'Sensor', 'DHT11 temperature and humidity sensor', 'DHT'],
    [11,  3, 22, 'Sensor', 'Tilt sensor', 'Tilt'],
    [13,  4, 23, 'Sensor', 'PIR(Passive Infrared Ray) Motion sensor', 'Motion'],
    [14,  5, 24, 'Sensor', 'Sound sensor', 'Sound'],
    [27, -1, -1, 'Sensor', 'Light intensity sensor', 'LightSensor'],
    [29, 27, 16, 'Sensor', 'Ultrasonic sensor', 'Ultrasonic'],

    [ 3, 29, 21, 'Other', 'Relay', 'Relay'],
    [ 6, -1, -1, 'Other', 'Raspberry Pi and PCBA connection switch'],
    [20,  1, 18, 'Other', 'Buzzer', 'Buzzer'],
    [40,  1, 18, 'Other', 'Touch Button And Buzzer', 'TouchButtonAndBuzzer'],
    [22,  2, 27, 'Other', 'Vibration motor', 'Vibration'],

    [15, 28, 20, 'I/F', 'IR sensor interface / Remote Controller', 'IR'],
    [51, 24, 19, 'I/F', 'Crowtail interface / Moisture', 'MoistureSensor'],
    [17, 24, 19, 'I/F', '9g servo interface', 'sg90'],
    [34, 24, 19, 'I/F', '9g servo interface / Like a Step Motor?', 'ServoMotor_LikeStep'],
    [18,  6, 25, 'I/F', 'Stepper motor interface', 'StepMotor'],

# Camera
# Microphone, Speacker, Earphone

# pinout cmd may help
# Connectivity
#  Wired LAN
#  Wireless LAN
#  Bluetooth
#  2.4GHz Keyboard & Mouse
#  USB 1/2/3/4

# storage
# df -m cmd

    [99, -1, -1, 'System', 'Execute ALL!', 'DUMMY'],
    [ 0, -1, -1, 'System', 'Exit this menu (or Ctrl+C)', 'DUMMY'],
]

import sys
import importlib
def default_menu():
    print('')
    print('CrowPi2 Sensor Tester')
    print('')
    print('     \tGP GPIO No.')
    print('     \t   BC BCM No.')
    print('     \t       [-] NOT Implemented Test Function...')

    print(' Cat.\tGP BC No Item')
    for item in menu_items:
        impl = '-' if len(item) == 5 else ' '
        gpio = '  ' if item[1] == -1 else str(item[1]).rjust(2, ' ')
        gpior = '  ' if item[2] == -1 else str(item[2]).rjust(2, ' ')
        # printf https://stackoverflow.com/questions/19457227/how-to-print-like-printf-in-python3/37848366#37848366
        sys.stdout.write(" %s\t%s %s %2d%s %s\n" % (item[3], gpio, gpior, item[0], impl, item[4]))
    print('')

    while True:
        print('Input No')
        menuno = int(input())

        for item in menu_items:
            if item[0] == 0 or item[0] == 99:
                sys.exit()

            if item[0] == menuno and len(item) == 5:
                print(str(menuno) + ' Not Implemented!')
                break

            if (item[0] == menuno or menuno == 99) and len(item) == 6:
                print('\n********** ********** ********** **********')
                print('[' + item[3] + '] - ' + item[4])
                # dynamic loading https://stackoverflow.com/questions/4821104/dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported-module/30941292#30941292
                MyClass = getattr(importlib.import_module("test_sensors"), item[5])
#                try:
                instance = MyClass()
#                except Exception as e:
#                    print(e)
#                    break

                try:
                    instance.main() # force execute main method without confirm imeplemented
                except AttributeError:
                    pass
                if menuno != 99:
                    sys.exit()

def main():
    default_menu()
    # or...
    # Select Menu Order
    # 1. Category(default)
    # 2. Official Document Number
    # 3. GPIO Real Assign Number (use coding)
    # 4. GPIO Number (schematic)

if __name__ == "__main__":
    main()

