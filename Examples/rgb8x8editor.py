#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import math # Step Motor
import random
import sys
import threading
import time
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk

# https://qiita.com/Kobayashi2019/items/03e31ee50b924f428e71
# don't create __pycache__
sys.dont_write_bytecode = True

# specific hardware
import platform
if getattr(platform.uname(), 'node') == 'raspberrypi':
    import Adafruit_CharLCD as LCD
    import Adafruit_DHT # Temperature
    from Adafruit_LED_Backpack import SevenSegment
    from rpi_ws281x import PixelStrip, Color # RGBMatrix
    import smbus  # LightSensor
    import spidev # ButtonMatrix, Joystick

######################################################################
# print('/usr/share/code/project/Tilt_reminder/Tilt_reminder.py')
class RGBMatrix:

    def __init__(self):
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

        #  0  1  2  3  4  5  6  7
        #  8  9 10 11 12 13 14 15
        # 16 17 18 19 20 21 22 23
        # 24 25 26 27 28 29 30 31
        # 32 33 34 35 36 37 38 39
        # 40 41 42 43 44 45 46 47
        # 48 49 50 51 52 53 54 55
        # 56 57 58 59 60 61 62 63
        self.numbers = [
            [0, 1, 2, 3, 4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8], # 0
            [3, 11, 19, 27, 35, 43, 51, 59], # 1
            [9, 2, 3, 4, 13, 21, 28, 28, 34, 41, 49, 57, 58, 59, 60, 61],     # 2
            [2, 3, 4, 13, 21, 28, 27, 26, 25, 37, 45, 53, 60, 59, 58, 57],    # 3
            [1, 9, 17, 25, 33, 41, 42, 43, 44, 45, 46, 47, 28, 36, 52, 60],   # 4
            [1, 9, 17, 25, 26, 27, 28, 29, 38, 46, 54, 61, 60, 59, 58, 57, 2, 3, 4, 5], # 5
            [6, 5, 4, 3, 2, 1, 9, 17, 25, 33, 41, 49, 57, 58, 59, 60, 61, 62, 54, 46, 38, 37, 36, 35, 34], # 6
            [1, 2, 3, 4, 5, 6, 7, 15, 22, 29, 36, 44, 52, 60],                # 7
            [4, 3, 2, 9, 18, 27, 36, 45, 53, 60, 59, 58, 49, 41, 34, 20, 13], # 8
            [7, 6, 5, 4, 3, 2, 1, 9, 17, 25, 33, 34, 35, 36, 37, 38, 39, 31, 23, 15, 47, 55, 63, 62, 61, 60, 59, 58, 57], # 9
            [16, 17, 18, 19, 20, 21, 22, 23, 40, 41, 42, 43, 44, 45, 46, 47, 2, 10, 26, 34, 50, 58, 5, 13, 29, 37, 53, 61], # 10 #
            [17, 18, 19, 20, 21, 22, 49, 50, 51, 52, 53, 54], # 11 =
            [28], # 12 -
            [26, 27, 28, 19, 35], # 13 +
            [7, 56, 14, 49, 21, 42, 28, 35], # 14 /
            [63, 54, 45, 36, 27, 35, 42, 49, 56, 0, 9, 18, 28, 21, 14, 7], # 15 X
        ]
        # or # color code
        #[0,  0,  0,  0,  0,  0,  0, 0,
        # 0,200,  0,  0, 70,  0,  0, 0,
        # 0,  0,  0,  0, 60,  0,  0, 0,
        # 0,  0,  0,  0, 50,  0,  0, 0,
        # 0, 10, 20, 30, 40, 30, 20, 0,
        # 0,  0,  0, 80,  0,  0,  0, 0,
        # 0,  0,  0, 90,  0,  0,  0, 0,
        # 0,  0,  0,100,  0,  0,  0, 0]

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def clear(self, r=0, g=0, b=0):
        self.colorWipe(Color(r, g, b), 5)

    def fill(self, col):
        self.colorWipe(col, 10)

    def rand(self):
        l = list(range(self.strip.numPixels()))
        random.shuffle(l)
        for i in l:
            self.strip.setPixelColor(i, Color(random.randint(10, 250), random.randint(10, 250), random.randint(10, 250)))
            self.strip.show()
            time.sleep(0.01)

    def dot(self, num, col):
        self.strip.setPixelColor(int(num), col)
        self.strip.show()

    def show_template(self, num, col):
        self.clear()
        for cell in self.numbers[int(num)]:
            self.strip.setPixelColor(cell, col)
        self.strip.show()

class RGBMatrixS: # Skelton
    def __init__(self): pass
    def clear(self): pass
    def fill(self, col): pass
    def rand(self): pass
    def dot(self, num, col): pass
    def show_template(self, num, col): pass

######################################################################
# this class merged into InputSensors # remained multi threads debugging
class TouchSensor():

    def __init__(self, _rgb, _seg):
        self.rgb = _rgb
        self.seg = _seg

        # define touch pin
        self.touch_pin = 17
        # set board mode to GPIO.BCM
        GPIO.setmode(GPIO.BCM)
        # set GPIO pin to INPUT
        GPIO.setup(self.touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.started = threading.Event()
        self.alive = True
        self._start_thread_main()

    def _start_thread_main(self):
        self.thread_main = threading.Thread(target=self._main_func)
        self.thread_main.start()
        self.started.set()

    def _main_func(self):
        self.started.wait()
        while self.alive:
            if self.started.is_set() == True:
                if(GPIO.input(self.touch_pin)):
                    self.rgb.clear()
                    self.seg.clear()
                    self.seg.write_display()
                    time.sleep(0.1)
                    print('aa-1')
            else:
                print('aa-2-1')
                self.started.wait()
                print('aa-2-2')
            pass

    def on_close(self): # TODO: How to close in safety
        self.started.clear()
        self.started.set()
        self.alive = False

        if self.started.is_set() == False:
            #self.started.set()
            self.alive = False
            #self.thread_main.join()
        else:
            #self.started.set()
            self.alive = False
            #self.thread_main.join()
        print('TouchSensor::on_close()')

######################################################################
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/touch.py')
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/motion.py')
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/sound.py')
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/IR_New.py')
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/dh11.py')
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/tilt.py')
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/distance.py')
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/light_sensor.py')
# print('/usr/share/code/project/Memory/Memory.py') # for Joystick
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/RFID/Read.py & MFRC522.py')

# Thread https://qiita.com/kotai2003/items/db7c846e0d4e2d6d6d45
class InputSensors():

    def __init__(self, _rgb, _seg):
        self.rgb = _rgb
        self.seg = _seg

        # set board mode to GPIO.BCM
        GPIO.setmode(GPIO.BCM)

        # define touch pin
        self.touch_pin = 17
        # set GPIO pin to INPUT
        GPIO.setup(self.touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.motion_pin = 23
        GPIO.setup(self.motion_pin, GPIO.IN)

        self.sound_pin = 24
        GPIO.setup(self.sound_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.ir_pin = 20
        GPIO.setup(self.ir_pin, GPIO.IN, GPIO.PUD_UP)

        self.ir_indexes = {
            0x45:'CH-',  0x46:'CH',   0x47:'CH+',
            0x44:'PREV', 0x40:'NEXT', 0x43:'PLAY',
            0x07:'VOL-', 0x15:'VOL+', 0x09:'EQ',
            0x16:'0',    0x19:'100+', 0x0d:'200+',
            0x0c:'1',    0x18:'2',    0x5e:'3',
            0x08:'4',    0x1c:'5',    0x5a:'6',
            0x42:'7',    0x52:'8',    0x4a:'9'
        }

        self.ir_last = 'No'

        self.tilt_pin = 22
        GPIO.setup(self.tilt_pin, GPIO.IN)

        self.TRIG = 16
        self.ECHO = 26 # CrowPi1 12
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

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

        self.MIFAREReader = None

    def _set_label(self, _mot, _snd, _ir, _temp, _tilt, _son, _lig, _toc, _rfid):
        self.mot = _mot
        self.snd = _snd
        self.ir  = _ir
        self.temp = _temp
        self.tilt = _tilt
        self.son = _son
        self.lig = _lig
        self.toc = _toc
        self.rfid = _rfid

    def _set_joy(self, _cb, _up, _le, _ce, _ri, _do):
        self.joy_cb = _cb
        self.joy_up = _up
        self.joy_le = _le
        self.joy_ce = _ce
        self.joy_ri = _ri
        self.joy_do = _do

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
        # Read the data
        x_value = self.ReadChannel(self.x_channel)
        y_value = self.ReadChannel(self.y_channel)

        self.joy_ce['text'] = "("+str(x_value)+", "+str(y_value)+")"
        self.joy_le['relief'] = tk.RAISED if x_value > 650 else tk.FLAT
        self.joy_ri['relief'] = tk.RAISED if x_value < 400 else tk.FLAT
        self.joy_up['relief'] = tk.RAISED if y_value > 650 else tk.FLAT
        self.joy_do['relief'] = tk.RAISED if y_value < 400 else tk.FLAT

        # Wait before repeating loop
        #time.sleep(self.delay)

    def _start_thread_main(self):
        self.started = threading.Event()
        self.alive = True
        #self._start_thread_main()

        self.thread_main = threading.Thread(target=self._main_func)
        self.thread_main.start()
        self.started.set()

    def decode_ir(self, key_val):
        if not key_val in self.ir_indexes:
            self.ir_last = 'Unknown'
            return self.ir_last
        return self.ir_indexes[key_val]

    def detect_ir(self):
        if GPIO.input(self.ir_pin) != 0:
            return self.ir_last

        count = 0
        while GPIO.input(self.ir_pin) == 0 and count < 200:
            count += 1
            time.sleep(0.00006)

        count = 0
        while GPIO.input(self.ir_pin) == 1 and count < 80:
            count += 1
            time.sleep(0.00006)

        idx = 0
        cnt = 0
        data = [0,0,0,0]
        for i in range(0,32):
            count = 0
            while GPIO.input(self.ir_pin) == 0 and count < 15:
                count += 1
                time.sleep(0.00006)

            count = 0
            while GPIO.input(self.ir_pin) == 1 and count < 40:
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
            #print("Get the key[0x%02x][%s]" % (data[2], self.decode(data[2])))
            self.ir_last = ("[0x%02x][%s]") % (data[2], self.decode_ir(data[2]))
        return self.ir_last

    # TODO: thread
    def get_temperature(self):
        sensor = 11
        pin = 4

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Un-comment the line below to convert the temperature to Fahrenheit.
        fahrenheit = temperature * 9/5.0 + 32

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        tmp = 'Failed to get'
        if humidity is not None and temperature is not None:
            #print('Temp={0:0.1f}C, {1:0.1f}F,  Humidity={2:0.1f}%'.format(temperature, fahrenheit, humidity))
            tmp = '{0:0.1f}C, {1:0.1f}F\nHumi={2:0.1f}%'.format(temperature, fahrenheit, humidity)

        return tmp

    # TODO: thread
    def get_distance(self):
        GPIO.output(self.TRIG, False)
        #print("Waiting For Sensor To Settle in 2 seconds")
        #time.sleep(2)

        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        while GPIO.input(self.ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(self.ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        return round(distance, 2)

    def convertToNumber(self, data):
        # Simple function to convert 2 bytes of data into a decimal number
        return ((data[1] + (256 * data[0])) / 1.2)

    def readLight(self):
        data = self.bus.read_i2c_block_data(self.DEVICE,self.ONE_TIME_HIGH_RES_MODE_1)
        return '{0:0.2f}'.format(self.convertToNumber(data))

    def detect_rfid(self):
        if self.MIFAREReader is None:
            # https://qiita.com/yuukiclass/items/88e9ac6c5a3b5ab56cc4
            try:
                import MFRC522
            except Exception as e:
                print(e)
                #url = 'https://raw.githubusercontent.com/Elecrow-RD/CrowPi/master/Examples/RFID/MFRC522.py'
                url = 'https://raw.githubusercontent.com/kensuke/CrowPi2/main/Examples/MFRC522.py' # delete trace log output
                print('downloading MFRC522.py from ' + url)
                import urllib.request # for python3
                urllib.request.urlretrieve(url, 'MFRC522.py')
                time.sleep(0.5) # a few rest

                try:
                    import MFRC522
                except Exception as e:
                    print(e)
                    return 'on Err ext-lib DL'

            # create the reader object
            self.MIFAREReader = MFRC522.MFRC522()
            if self.MIFAREReader is None:
                return 'on Err H/W?'

        # detect touch of the card, get status and tag type
        (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        # check if card detected or not
        if status != self.MIFAREReader.MI_OK:
            return 'Not Found['+str(status)+']'

        # Get the RFID card uid and status
        (status,uid) = self.MIFAREReader.MFRC522_Anticoll()

        # If status is alright, continue to the next stage
        if status != self.MIFAREReader.MI_OK:
            return 'on Err Get UID'

        # Print UID
        uidstr = ("[%s,%s,%s,%s]" % (uid[0], uid[1], uid[2], uid[3]))
        # standard key for rfid tags
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        # Select the scanned tag
        self.MIFAREReader.MFRC522_SelectTag(uid)
        # authenticate
        status = self.MIFAREReader.MFRC522_Auth(self.MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        # check if authenticated successfully, read the data
        if status == self.MIFAREReader.MI_OK:
            self.MIFAREReader.MFRC522_Read(8)
            self.MIFAREReader.MFRC522_StopCrypto1()
            return 'OK ' + uidstr
        else:
            return 'on Err Auth ' + uidstr

    def _main_func(self):
        try:
            self.started.wait()
            while self.alive:
                if self.started.is_set() == True:

                    if self.toc[0].get():                  # Touch for reset
                        if(GPIO.input(self.touch_pin)):
                            self.rgb.clear()           # Clear RGB & 7-Seg
                            self.seg.clear()
                            self.seg.write_display()
                            self.toc[2]['text'] = 'Detected'
                        else:
                            self.toc[2]['text'] = ''

                    if self.mot[0].get():                  # Motion
                        mot = GPIO.input(self.motion_pin)
                        self.mot[2]['text'] = 'Detected' if mot else ''

                    if self.snd[0].get():                  # Sound
                        snd = GPIO.input(self.sound_pin) == GPIO.LOW
                        self.snd[2]['text'] = 'Detected' if snd else 'Silence'

                    if self.ir[0].get():                   # IR remote controller
                        self.ir[2]['text'] = self.detect_ir()

                    if self.temp[0].get():                 # Temperature
                        self.temp[2]['text'] = self.get_temperature()

                    if self.tilt[0].get():                 # Tilt
                        tilt = GPIO.input(self.tilt_pin) # positive is tilt to left negative is tilt to right
                        self.tilt[2]['text'] = '<--['+str(tilt)+']' if tilt else '['+str(tilt)+']-->'

                    if self.son[0].get():                  # Ultrasoic distance
                        self.son[2]['text'] = str(self.get_distance()) + " cm"

                    if self.lig[0].get():                  # Light
                        self.lig[2]['text'] = str(self.readLight()) + " lx"

                    if self.rfid[0].get():                 # RFID
                        self.rfid[2]['text'] = self.detect_rfid()

                    if self.joy_cb.get():                  # Joystick
                        self.sprite()

                    time.sleep(0.1)
                else:
                    self.started.wait()
                pass
        except KeyboardInterrupt: # TODO: how to interrupt?
            self.alive = False
            self.on_close()

    def on_close(self):
        self.started.clear()
        self.alive = False
        #self.started.set()
        #self.thread_main.join()

class InputSensorsS(): # Skelton
    def __init__(self, _rgb, _seg): pass
    def _set_label(self, _mot, _snd, _ir, _temp, _tilt, _son, _lig, _toc, _rfid): pass
    def _set_joy(self, cb, up, le, ce, ri, do): pass
    def _start_thread_main(self): pass
    def on_close(self): pass

######################################################################
# print('/usr/share/code/project/Calculator/Calculator.py')
class ButtonMatrix():

    def __init__(self, _rgb):
        self.rgb = _rgb

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

#        self.indexes = {
#            12:7, 13:8,  14:9,  15:'x',
#             8:4,  9:5,  10:6,  11:'/',
#             4:1,  5:2,   6:3,   7:'+',
#             0:0,  1:'#', 2:'=', 3:'-'
#        }

        self.indexes = {
            12:7, 13:8,  14:9,  15:15,
             8:4,  9:5,  10:6,  11:14,
             4:1,  5:2,   6:3,   7:13,
             0:0,  1:10,  2:11,  3:12
        }

        self.started = threading.Event()
        self.alive = True
        self._start_thread_main()

    def _start_thread_main(self):
        self.thread_main = threading.Thread(target=self._main_func)
        self.thread_main.start()
        self.started.set()

    def on_close(self):
        self.alive = False
        if self.started.is_set() == False:
            self.started.set()
            self.thread_main.join()
        else:
            self.started.clear()
            self.started.set()

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
        #print("button %s pressed" % btnIndex)
        self.rgb.show_template(btnIndex, get_color())
        # prevent button presses too close together
        time.sleep(.3)

    def _main_func(self):
        self.started.wait()
        while self.alive:
            if self.started.is_set() == True:
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
            else:
                self.started.wait()
        pass

class ButtonMatrixS(): # Skelton
    def __init__(self, _rgb): pass
    def on_close(self): pass

######################################################################
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/servo.py')
# print('Original Author Github: https://github.com/WindVoiceVox/Raspi_SG90')
class Servo():

    def __init__(self):
        self.pin = 19 # CrowPi1 25
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.direction = 0
        self.servo = GPIO.PWM(self.pin, 50) # Freq = 50Hz
        self.servo.start(0.0)
        self.servo.ChangeDutyCycle(self.conv(0))

    def cleanup(self):
        if self.servo:
            self.servo.ChangeDutyCycle(self.conv(-90))
            time.sleep(0.3)
            self.servo.stop()
        #GPIO.cleanup()

    # https://jellyware.jp/kurage/raspi/servo.html
    def conv(self, degree):
        degree = min(max(-90, degree), 90)
        return 2.5 + ( 12.0 - 2.5 ) / 180 * ( degree + 90 )

    def _henkan(self, value):
        return 0.05 * value + 7.0

    def setdirection(self, direction, speed):
        if self.servo is None:
            self.servo = GPIO.PWM(self.pin, 50)
            self.servo.start(0.0)

#        for d in range( self.direction, direction, int(speed) ):
#            self.servo.ChangeDutyCycle( self._henkan( d ) )
#            self.direction = d
#            time.sleep(0.1)
#            print(self.direction, self._henkan( self.direction ))

        if self.direction > direction:
            speed = (-1) * speed
        for d in range(self.direction, direction, speed):
            self.servo.ChangeDutyCycle(self.conv(d))
            time.sleep(0.1)
        self.servo.ChangeDutyCycle(0)
        self.direction = direction

class ServoS: # Skelton
    def __init__(self): pass
    def cleanup(self): pass
    def setdirection(self, direction, speed): pass

######################################################################
# print('/usr/share/code/project/Lucky_turntable')
class StepMotor():

    def __init__(self):
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

######################################################################
# global vars

root = tk.Tk()

# native
if getattr(platform.uname(), 'node') == 'raspberrypi':
    rgb = RGBMatrix()
    but = ButtonMatrix(rgb)
    seg = SevenSegment.SevenSegment(address=0x70)
    inputs = InputSensors(rgb, seg)
    lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
    servo = Servo()
else:
    # Skelton code for test on non-pi environment
    class Color():
        def __init__(self, r, g, b): pass

    class SevenSegment():
        def SevenSegment(address): return SevenSegment()
        def __init__(self): self.buffer = [0, 0, 0, 0, 0, 0, 0, 0]
        def begin(self): pass
        def clear(self): pass
        def write_display(self): pass

    class LCD():
        def Adafruit_CharLCDBackpack(address): return LCD()
        def __init__(self): pass
        def home(self): pass
        def clear(self): pass
        def set_cursor(self, col, row): pass
        def show_cursor(self, show): pass
        def blink(self, blink): pass
        def move_left(self): pass
        def move_right(self): pass
        def set_left_to_right(self): pass
        def set_right_to_left(self): pass
        def autoscroll(self, autoscroll): pass
        def message(self, text): pass
        def set_backlight(self, backlight): pass

    rgb = RGBMatrixS()
    but = ButtonMatrixS(rgb)
    seg = SevenSegment.SevenSegment(address=0x70)
    inputs = InputSensorsS(rgb, seg)
    lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
    servo = ServoS()

seg.begin()
seg.clear()

lcd.home()
lcd.clear()
lcd.set_backlight(0) # on

color = tk.StringVar(value='RND')
r_var_scale = tk.IntVar()
g_var_scale = tk.IntVar()
b_var_scale = tk.IntVar()

######################################################################
# functions

# on_close: https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
def on_close():
    servo.cleanup()
    inputs.on_close()
    lcd.clear()
    lcd.set_backlight(1) # off
    seg.clear()
    seg.write_display()
    but.on_close()
    rgb.clear()
    GPIO.cleanup()
    root.destroy()

def get_color():
    r, g, b = 0, 0, 0
    if color.get() == 'RND':
        r, g, b = random.randint(10, 250), random.randint(10, 250), random.randint(10, 250)
    else:
        r, g, b = r_var_scale.get(), g_var_scale.get(), b_var_scale.get()
    return Color(r, g, b)

######################################################################
# output

# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/vibration.py')
def vibration():
    # define vibration pin
    vibration_pin = 27
    # Set board mode to GPIO.BCM
    GPIO.setmode(GPIO.BCM)
    # Setup vibration pin to OUTPUT
    GPIO.setup(vibration_pin, GPIO.OUT)

    # turn on vibration
    GPIO.output(vibration_pin, GPIO.HIGH)
    # wait a second
    time.sleep(1)

    # turn off vibration
    GPIO.output(vibration_pin, GPIO.LOW)

    # cleaup GPIO
    #GPIO.cleanup()

# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/buzzer.py')
def buzzer():
    buzzer_pin = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    # Make buzzer sound
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(1)

    # Stop buzzer sound
    GPIO.output(buzzer_pin, GPIO.LOW)

    #GPIO.cleanup()

def b_and_v():
    buzzer_pin = 18
    vibration_pin = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.setup(vibration_pin, GPIO.OUT)

    GPIO.output(buzzer_pin, GPIO.HIGH)
    GPIO.output(vibration_pin, GPIO.HIGH)
    time.sleep(1)

    GPIO.output(buzzer_pin, GPIO.LOW)
    GPIO.output(vibration_pin, GPIO.LOW)

    #GPIO.cleanup()

######################################################################
# GUI
'''
 _   _    _   _ 
|_| |_| :|_| |_|
|_|.|_|.:|_|.|_|.

'''
def create_seven_seg_frame(top):
    # manipulate buffer dynamically
    # https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/Adafruit_LED_Backpack/SevenSegment.py
    def set_seven_seg(pos, mask, poi = False):
        pos = pos if pos < 2 else pos-1 #  fix pos 3 -> 2, 4 -> 3 ([0, 1, 3, 4] passed this function for colon[pos=2])
        pos = pos*2                     # conv pos 0 -> 0, 1 -> 2, 2->4, 3 -> 6
        if poi:
            mask = (1 << 7)
            # Point Position [x 0 4 6] # 2 = colon[:]
            if pos == 0:
                print('Unsupported This Position!! (maybe bug)')
                return
            elif pos == 2:
                pos = 0

        if seg.buffer[pos] & mask == 0:
            seg.buffer[pos] |= mask
        else:
            seg.buffer[pos] ^= mask
        seg.write_display()

    def show_colon():
        if seg.buffer[2] & (1 << 7) == 0:
            seg.buffer[2] |= (1 << 7)
        else:
            seg.buffer[2] ^= (1 << 7)
        seg.write_display()

    def fill_seg(rand = False):
        seg.buffer[0] = 0xFF
        seg.buffer[2] = 0xFF
        seg.buffer[4] = 0xFF
        seg.buffer[6] = 0xFF

        if rand:
            seg.buffer[0] ^= random.randint(0, 255)
            seg.buffer[2] ^= random.randint(0, 255)
            seg.buffer[4] ^= random.randint(0, 255)
            seg.buffer[6] ^= random.randint(0, 255)

        seg.write_display()

    def clear_seg():
        seg.clear()
        seg.write_display()

    def create_seg_frame(fr, r, c):
        inner = tk.Frame(fr, bd=2, relief=tk.SUNKEN)
        inner.grid(row=r, column=c)

        '''
           0x01
        0x20  0x02
           0x40
        0x10  0x04
           0x08
        '''
        button = tk.Button(inner, text='', command=lambda: set_seven_seg(c, 0x01))
        button.grid(row=0, column=1)
        button = tk.Button(inner, text='', command=lambda: set_seven_seg(c, 0x20))
        button.grid(row=1, column=0)
        button = tk.Button(inner, text='', command=lambda: set_seven_seg(c, 0x02))
        button.grid(row=1, column=2)
        button = tk.Button(inner, text='', command=lambda: set_seven_seg(c, 0x40))
        button.grid(row=2, column=1)
        button = tk.Button(inner, text='', command=lambda: set_seven_seg(c, 0x10))
        button.grid(row=3, column=0)
        button = tk.Button(inner, text='', command=lambda: set_seven_seg(c, 0x04))
        button.grid(row=3, column=2)
        button = tk.Button(inner, text='', command=lambda: set_seven_seg(c, 0x08))
        button.grid(row=4, column=1)
        button = tk.Button(inner, text='.', command=lambda: set_seven_seg(c, 0x00, True))
        button.grid(row=4, column=2)

    in_top = tk.Frame(top, bd=2, relief=tk.SUNKEN)
    in_top.grid(row=0, column=0, columnspan=2)

    dig0 = create_seg_frame(in_top, 0, 0)
    dig1 = create_seg_frame(in_top, 0, 1)
    colon = tk.Button(in_top, text=':', command=lambda: show_colon())
    colon.grid(row=0, column=2)
    dig2 = create_seg_frame(in_top, 0, 3) # 2
    dig3 = create_seg_frame(in_top, 0, 4) # 3

    # command button
    in_bot = tk.Frame(top, bd=2, relief=tk.SUNKEN)
    in_bot.grid(row=1, column=0, columnspan=2)

    button = tk.Button(in_bot, text='FILL',  command=lambda: fill_seg())
    button.grid(row=0, column=0)
    button = tk.Button(in_bot, text='RAND',  command=lambda: fill_seg(True))
    button.grid(row=0, column=1)
    button = tk.Button(in_bot, text='CLEAR', command=lambda: clear_seg())
    button.grid(row=0, column=2)

# | 8x8 | sel | color c |
# |     | rgb | scalex3 |
# |     | rnd |         |
# |     |    fill clear |
def create_rgb8x8_frame(top):
# LEFT
    left = tk.Frame(top, bd=2, relief=tk.SUNKEN)
    left.grid(row=1, column=0)

    def on_rgb_button_pressed(id):
        rgb.dot(id, get_color())

    def create_rgb_button(frame, x, y):
        pos = y * 8 + x
        button = tk.Button(frame, text=' ', command=lambda: on_rgb_button_pressed(str(pos)))
        button.grid(row=y, column=x)

    for y in range(0, 8):
        for x in range(0, 8):
            create_rgb_button(left, x, y)

# RIGHT
    # R
    right = tk.Frame(top, bd=2, relief=tk.SUNKEN)
    right.grid(row=1, column=1)

    # R-L radio area
    inframe1 = tk.Frame(right, bd=1, relief=tk.SUNKEN)
    inframe1.grid(row=0, column=0)

    color_sel = tk.Radiobutton(inframe1, text='sel', variable=color, value='SEL')
    color_rgb = tk.Radiobutton(inframe1, text='rgb', variable=color, value='RGB')
    color_rnd = tk.Radiobutton(inframe1, text='rnd', variable=color, value='RND')
    color_sel.grid(row=0, column=0)
    color_rgb.grid(row=1, column=0)
    color_rnd.grid(row=2, column=0)

    # R-R
    inframe2 = tk.Frame(right, bd=1, relief=tk.SUNKEN)
    inframe2.grid(row=0, column=1)

    # R-R-1 # color chooser area
    def sel_col():
        c = colorchooser.askcolor()
        if c[0] == None:
            return

        r_var_scale.set(int(c[0][0]))
        g_var_scale.set(int(c[0][1]))
        b_var_scale.set(int(c[0][2]))

    button = tk.Button(inframe2, text='SELECT', command=sel_col)
    button.grid(row=0, column=0)

    # R-R-2 # RGB scale area
    r_var_scale.set(0)
    r_scale = tk.Scale(inframe2, variable=r_var_scale, orient=tk.HORIZONTAL, to=255)
    r_scale.grid(row=1, column=0)

    g_var_scale.set(0)
    g_scale = tk.Scale(inframe2, variable=g_var_scale, orient=tk.HORIZONTAL, to=255)
    g_scale.grid(row=2, column=0)

    b_var_scale.set(0)
    b_scale = tk.Scale(inframe2, variable=b_var_scale, orient=tk.HORIZONTAL, to=255)
    b_scale.grid(row=3, column=0)

    # R-R-3 button area
    inframe3 = tk.Frame(right, bd=1, relief=tk.SUNKEN)
    inframe3.grid(row=1, column=0, columnspan=2)

    button = tk.Button(inframe3, text='FILL',  command=lambda: rgb.fill(get_color()))
    button.grid(row=0, column=0)
    button = tk.Button(inframe3, text='RAND',  command=lambda: rgb.rand())
    button.grid(row=0, column=1)
    button = tk.Button(inframe3, text='CLEAR', command=lambda: rgb.clear())
    button.grid(row=0, column=2)

# Several Sensors Status Window
r = 0
def create_sensor_frame(top):

    def create_sensor_label(_txt, checked=True):
        global r
        b = tk.BooleanVar(value=checked)
        cb = tk.Checkbutton(top, text=_txt, variable=b)
        cb.grid(row=r, column=0)
        lr = tk.Label(top, bd=1)
        lr.grid(row=r, column=1)
        lr['text'] = _txt
        r += 1
        return [b, cb, lr]

    mot = create_sensor_label('Motion')
    snd = create_sensor_label('Sound')
    ir  = create_sensor_label('IR')
    temp = create_sensor_label('Temp', False) # because every measurement needs 2 seconds.. and main thread stopped.
    tilt = create_sensor_label('Tilt')
    son = create_sensor_label('Sonic')
    lig = create_sensor_label('Light')
    toc = create_sensor_label('Touch')
    rfid= create_sensor_label('RFID')

    def dummy_func_for_default_checked(): # TODO: What's This!?
        mot[0].get()
        snd[0].get()
        ir[0].get()
        temp[0].get()
        tilt[0].get()
        son[0].get()
        lig[0].get()
        toc[0].get()
        rfid[0].get()
    button = tk.Button(top, text='NINJA BUTTON', command=dummy_func_for_default_checked) # comment out this line, then check off!

    inputs._set_label(mot, snd, ir, temp, tilt, son, lig, toc, rfid)

# Buzzer, Vibration, Relay, Servo Motor, Step Motor
def create_output_frame(top):
    button = tk.Button(top, text='Buzzer', command=buzzer)
    button.grid(row=0, column=0)

    button = tk.Button(top, text='BOTH', command=b_and_v)
    button.grid(row=0, column=1)

    button = tk.Button(top, text='Vibration', command=vibration)
    button.grid(row=0, column=2)

# Relay
    # print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/relay.py')
    relf = tk.LabelFrame(top, bd=2, relief=tk.SUNKEN, text='Relay')
    relf.grid(row=1, column=0, columnspan=3)

    relay = tk.StringVar(value='Open')
    def onoff_relay():
        cmd = relay.get()
        # define relay pin
        relay_pin = 21
        if cmd == 'Open':
            # set GPIO mode as GPIO.BCM
            GPIO.setmode(GPIO.BCM)
            # setup relay pin as OUTPUT
            GPIO.setup(relay_pin, GPIO.OUT)
            # Open Relay
            GPIO.output(relay_pin, GPIO.LOW) # first time low signal is open?
        elif cmd == 'High':
            GPIO.output(relay_pin, GPIO.HIGH)
        elif cmd == 'Low':
            GPIO.output(relay_pin, GPIO.LOW)
        else:
            GPIO.output(relay_pin, GPIO.LOW)
            #GPIO.cleanup()

    relay_op = tk.Radiobutton(relf, text='Open',  variable=relay, value='Open',  command=onoff_relay)
    relay_hi = tk.Radiobutton(relf, text='High',  variable=relay, value='High',  command=onoff_relay)
    relay_lo = tk.Radiobutton(relf, text='Low',   variable=relay, value='Low',   command=onoff_relay)
    relay_cl = tk.Radiobutton(relf, text='Close', variable=relay, value='Close', command=onoff_relay)

    relay_op.grid(row=0, column=0)
    relay_hi.grid(row=0, column=1)
    relay_lo.grid(row=0, column=2)
    relay_cl.grid(row=0, column=3)

# Servo Motor
    serv = tk.LabelFrame(top, bd=2, relief=tk.SUNKEN, text='Servo Motor')
    serv.grid(row=2, column=0, columnspan=3)

    dirs = [-90, -60, -45, -30, 0, 30, 45, 60, 90]
    cmb_dir = ttk.Combobox(serv, values=dirs, width=5)
    cmb_dir.grid(row=0, column=0)
    cmb_dir.state(['readonly'])
    cmb_dir.set(0)
    #cmb_dir.bind('<<ComboboxSelected>>', selected_dir)

    speed = [1, 5, 9, 19, 29]
    cmb_spd = ttk.Combobox(serv, values=speed, width=5)
    cmb_spd.grid(row=0, column=1)
    cmb_spd.state(['readonly'])
    cmb_spd.set(9)
    #cmb_spd.bind('<<ComboboxSelected>>', selected_spd)

    def run_serv():
        servo.setdirection( int(cmb_dir.get()), int(cmb_spd.get()) )

    button = tk.Button(serv, text='Run', command=run_serv)
    button.grid(row=0, column=2)

# Step Motor
    step = tk.LabelFrame(top, bd=2, relief=tk.SUNKEN, text='Step Motor')
    step.grid(row=3, column=0, columnspan=3)

    turn = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    cmb_turn = ttk.Combobox(step, values=turn, width=5)
    cmb_turn.grid(row=0, column=0)
    cmb_turn.state(['readonly'])
    cmb_turn.set(1)

    def run_step():
        stepm = StepMotor()
        stepm.turnDegrees(360*int(cmb_turn.get()))

    button = tk.Button(step, text='Run', command=run_step)
    button.grid(row=0, column=1)

# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/lcd.py')
def create_lcd_frame(top):

    # https://qiita.com/haruyan_hopemucci/items/6718188c7820336e6900
    # https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback
    class ModifiedEntry(tk.Entry):
        def __init__(self, *args, **kwargs):
            tk.Entry.__init__(self, *args, **kwargs)
            self.sv = tk.StringVar()
            self.sv.trace('w',self.var_changed)
            self.configure(textvariable = self.sv)

        def var_changed(self, *args):
            if args[0] == self.sv._name:
                s = self.sv.get()
                self.event_generate("<<TextModified>>")

    entry1 = ModifiedEntry(top)
    entry1.insert(0, 'Hello, world!!16')
    entry1.grid(row=0, column=0)
    lcd.message('Hello, world!!16')

    entry2 = ModifiedEntry(top)
    entry2.grid(row=1, column=0)

    def on_change(event):
        #print(event.widget.get())
        msg = entry1.get() + '\n' + entry2.get()
        lcd.home()
        lcd.clear()
        lcd.message(msg)
    entry1.bind("<<TextModified>>", on_change)
    entry2.bind("<<TextModified>>", on_change)

    button = tk.Button(top, text='CLEAR', command=lambda: lcd.clear())
    button.grid(row=0, column=1)

    bli = tk.BooleanVar(value=True)
    cbli = tk.Checkbutton(top, text='LIGHT',  variable=bli, command=lambda: lcd.set_backlight(0 if bli.get() else 1)) # on 0, off 1
    cbli.grid(row=0, column=2)

    bcu = tk.BooleanVar(value=False)
    cbcu = tk.Checkbutton(top, text='CURSOR', variable=bcu, command=lambda: lcd.show_cursor(bcu.get()))
    cbcu.grid(row=0, column=3)

    bbl = tk.BooleanVar(value=False)
    cbbl = tk.Checkbutton(top, text='BLINK',  variable=bbl, command=lambda: lcd.blink(bbl.get()))
    cbbl.grid(row=0, column=4)

    lcd_sc = tk.StringVar(value='=')
    def onoff_lcd_sc():
        cmd = lcd_sc.get()

        if cmd == '<-':
            lcd.move_left()
        elif cmd == '=':
            lcd.home()
            #lcd.autoscroll(True)
        elif cmd == '->':
            lcd.move_right()

    radf = tk.Frame(top)
    radf.grid(row=1, column=1, columnspan=3)

    en_ls = tk.Radiobutton(radf, text='<-', variable=lcd_sc, value='<-', command=onoff_lcd_sc)
    en_au = tk.Radiobutton(radf, text='=',  variable=lcd_sc, value='=',  command=onoff_lcd_sc)
    en_rs = tk.Radiobutton(radf, text='->', variable=lcd_sc, value='->', command=onoff_lcd_sc)

    en_ls.grid(row=1, column=1)
    en_au.grid(row=1, column=2)
    en_rs.grid(row=1, column=3)

    blr = tk.BooleanVar(value=False)
    def left_or_right():
        if blr:
            lcd.set_right_to_left()
        else:
            lcd.set_left_to_right()
        lcd.home()
    cblr = tk.Checkbutton(top, text='RIGHT',  variable=blr, command=lambda: left_or_right())
    cblr.grid(row=1, column=4)

'''
        # Define LCD column and row size for 16x2 LCD.
        lcd_columns = 16
        lcd_rows    = 2

        message = 'Scroll'
        lcd.message(message)
        for i in range(lcd_columns-len(message)):
        for i in range(lcd_columns-len(message)):
'''

# GUI builder
# [segf] | [senf]
# -------+-------
# [rgbf] | [joy_and_outf]
# -------+-------
# [lcdf] |
def create_frame(frame):
# 7seg
    segf = tk.LabelFrame(frame, bd=2, relief=tk.SUNKEN, text='7 Seg * 4 Digits LED')
    segf.grid(row=0, column=0)#, columnspan=2)
    create_seven_seg_frame(segf)

# 8x8 RGB Matrix
    rgbf = tk.LabelFrame(frame, bd=2, relief=tk.SUNKEN, text='RGB 8*8 Matrix')
    rgbf.grid(row=1, column=0)
    create_rgb8x8_frame(rgbf)

# input sensors status area!?
    senf = tk.LabelFrame(frame, bd=2, relief=tk.SUNKEN, text='Sensors Status')
    senf.grid(row=0, column=1)
    create_sensor_frame(senf)

# joystick & output component
    joy_and_outf = tk.Frame(frame, bd=2)
    joy_and_outf.grid(row=1, column=1)

    joyf = tk.LabelFrame(joy_and_outf, bd=2, relief=tk.SUNKEN, text='Joystick')
    joyf.grid(row=0, column=0)

    b = tk.BooleanVar(value=True)
    cb = tk.Checkbutton(joyf, variable=b)
    cb.grid(row=0, column=0)
    button = tk.Button(joyf, text='NINJA BUTTON', command=lambda: b.get()) # comment out this line, then check off!

    up = tk.Label(joyf, text='y > 650')
    le = tk.Label(joyf, text='x > 650')
    ce = tk.Label(joyf, text='')
    ri = tk.Label(joyf, text='x < 400')
    do = tk.Label(joyf, text='y < 400')
    up.grid(row=0, column=1)
    le.grid(row=1, column=0)
    ce.grid(row=1, column=1)
    ri.grid(row=1, column=2)
    do.grid(row=2, column=1)
    inputs._set_joy(b, up, le, ce, ri, do)

    outf = tk.LabelFrame(joy_and_outf, bd=2, relief=tk.SUNKEN, text='Output Devices')
    outf.grid(row=1, column=0)
    create_output_frame(outf)

# LCD
    lcdf = tk.LabelFrame(frame, bd=2, relief=tk.SUNKEN, text='LCD 16*2')
    lcdf.grid(row=2, column=0)
    create_lcd_frame(lcdf)

# TODO:
# code area
# 8*8 Dot Picture Save & Load
#class RFIDReader():

def main():
    root.title('CrowPi2 RGB Matrix Editor')
    root.protocol('WM_DELETE_WINDOW', on_close)

    top = tk.Frame(root, bd=2, relief=tk.SUNKEN)
#    top.grid_rowconfigure(0, weight=1)
#    top.grid_columnconfigure(0, weight=1)
#    top.pack(fill=tk.BOTH,expand=1)
    top.grid()
    create_frame(top)

    inputs._start_thread_main()

    root.mainloop()

if __name__ == "__main__":
    main()
