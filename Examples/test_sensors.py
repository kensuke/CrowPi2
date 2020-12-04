#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : original author Elecrow

###############################################################################
# DATA Definition                                                             #
###############################################################################
gpio_pins = [
    #PH  GP  GR  DESC          PH  GP  GR  DESC        # Always ON
    [ 1, -1, -1, '3V3'],      [ 2, -1, -1, '5V'],      # * *
    [ 3, -1,  2, 'SDA1'],     [ 4, -1, -1, '5V'],      #   *
    [ 5, -1,  3, 'SCL1'],     [ 6, -1, -1, 'GND'],
    [ 7, -1,  4, '1Wire'],    [ 8, -1, 14, 'TxD'],
    [ 9, -1, -1, 'GND'],      [10, -1, 15, 'RxD'],
    [11,  0, 17, 'Touch'],    [12,  1, 18, 'Buzzer'],
    [13,  2, 27, 'Vib'],      [14, -1, -1, 'GND'],
    [15,  3, 22, 'Tilt'],     [16,  4, 23, 'Motion?'], # * *blink
    [17, -1, -1, '3V3'],      [18,  5, 24, 'Sound'],   # *
    [19, -1, 10, 'MOSI'],     [20, -1, -1, 'GND'],
    [21, -1,  9, 'MISO'],     [22,  6, 25, 'Servo-M'],
    [23, -1, 11, 'SCLK'],     [24, -1,  8, 'CE0'],
    [25, -1, -1, 'GND'],      [26, -1,  7, 'CE1'],
    [27, -1,  0, 'SDA0'],     [28, -1,  1, 'SCL0'],    # *
    [29, 21,  5, 'Step-M-1'], [30, -1, -1, 'GND'],
    [31, 22,  6, 'Step-M-2'], [32, 26, 12, 'RGB Matrix'],
    [33, 23, 13, 'Step-M-3'], [34, -1, -1, 'GND'],
    [35, 24, 19, 'Step-M-4'], [36, 27, 16, 'Ultrasonic-TRIG'],
    [37, 25, 26, 'Uls-ECHO'], [38, 28, 20, 'IR'],
    [39, -1, -1, 'GND'],      [40, 29, 21, 'Relay'],
]

###############################################################################
# INPUT                                                                       #
###############################################################################

# /usr/share/code/project/Calculator/Calculator.py
class ButtonMatrix():
# Author : original author stenobot
# Original Author Github: https://github.com/stenobot/SoundMatrixPi

    def __init__(self):
        import RPi.GPIO as GPIO
        import time
        import spidev

        # Open SPI bus
        self.spi = spidev.SpiDev()
        self.spi.open(0,1)
        self.spi.max_speed_hz=1000000

        GPIO.setmode(GPIO.BCM)

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
            GPIO.cleanup()

# touch.py
class TouchSensor():

    def __init__(self):
        import RPi.GPIO as GPIO
        import time

        print('Touch Button')

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

###############################################################################
# OUTPUT                                                                      #
###############################################################################

# segment.py
class FourDigitSegment():

    def __init__(self):
        import time
        import datetime
        from Adafruit_LED_Backpack import SevenSegment

        # ===========================================================================
        # Clock Example
        # ===========================================================================
        segment = SevenSegment.SevenSegment(address=0x70)

        # Initialize the display. Must be called once before using the display.
        segment.begin()

        for i in range(10):
            segment.set_digit(0, i)
            segment.set_digit(1, (i+1)%10)
            segment.set_digit(2, (i+2)%10)
            segment.set_digit(3, (i+3)%10)
            segment.write_display()
            time.sleep(0.2)

        print("Press CTRL+C to exit")

        # Continually update the time on a 4 char, 7-segment display
        try:
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

# blinking_led.py
class GPIOLed():

    def __init__(self):
        import time
        import RPi.GPIO as GPIO

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

# BUG: i2c timeout after this test. AT YOUR OWN RISK!
class GPIOLed_DONOT_USE():

    def __init__(self):
        import time
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BOARD)    

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
                    pin_o = gpio_pins[pins * 2]
                    pin_e = gpio_pins[pins * 2 + 1]

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

# lcd.py
class LCD1602():

    def __init__(self):
        # Example using a character LCD backpack.
        import time
        import Adafruit_CharLCD as LCD

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

###############################################################################
# Sensor                                                                      #
###############################################################################

# dh11.py
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
        import sys
        import Adafruit_DHT

        # set type of the sensor
        sensor = 11
        # set pin number
        pin = 4

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Un-comment the line below to convert the temperature to Fahrenheit.
        # temperature = temperature * 9/5.0 + 32

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')

# tilt.py
class Tilt():

    def __init__(self):
        import time
        import RPi.GPIO as GPIO

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

# motion.py
class Motion():

    def __init__(self):
        import RPi.GPIO as GPIO
        import time

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

# sound.py
class Sound():

    def __init__(self):
        import RPi.GPIO as GPIO
        import time

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
                    print('Sound of silence')
                time.sleep(0.1)
        except KeyboardInterrupt:
            # CTRL+C detected, cleaning and quitting the script
            GPIO.cleanup()

# light_sensor.py
class LightSensor():
# Author: Matt Hawkins
# Author's Git: https://bitbucket.org/MattHawkinsUK/
# Author's website: https://www.raspberrypi-spy.co.uk

    def __init__(self):
        import RPi.GPIO as GPIO
        import smbus

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
        import time
        try:
            while True:
                print("Light Level : " + str(self.readLight()) + " lx")
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass

# distance.py
class Ultrasonic():
# Author : www.modmypi.com
# Link: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

    def __init__(self):
        import RPi.GPIO as GPIO
        import time

        GPIO.setmode(GPIO.BCM)

        TRIG = 16
        ECHO = 26 # CrowPi1 12

        print("Distance Measurement In Progress")

        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)

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

        GPIO.cleanup()

###############################################################################
# Hardware                                                                    #
###############################################################################

# relay.py
class Relay():

    def __init__(self):
        import RPi.GPIO as GPIO
        import time

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

# buzzer.py
class Buzzer():

    def __init__(self):
        import RPi.GPIO as GPIO
        import time

        buzzer_pin = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer_pin, GPIO.OUT)

        # Make buzzer sound
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(0.5)

        # Stop buzzer sound
        GPIO.output(buzzer_pin, GPIO.LOW)

        GPIO.cleanup()

# button_buzzer.py
class TouchButtonAndBuzzer():

    def __init__(self):
        import RPi.GPIO as GPIO

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

# vibration.py
class Vibration():

    def __init__(self):
        import RPi.GPIO as GPIO
        import time

        # define vibration pin
        vibration_pin = 27
        # Set board mode to GPIO.BCM
        GPIO.setmode(GPIO.BCM)
        # Setup vibration pin to OUTPUT
        GPIO.setup(vibration_pin, GPIO.OUT)

        # turn on vibration
        GPIO.output(vibration_pin, GPIO.HIGH)

        # wait half a second
        time.sleep(0.5)

        # turn off vibration
        GPIO.output(vibration_pin, GPIO.LOW)

        # cleaup GPIO
        GPIO.cleanup()

###############################################################################
# Interface                                                                   #
###############################################################################

import time
import RPi.GPIO as GPIO
import math

# stepmotor.py
class ServoMotor():
# Author : Original author ludwigschuster
# Original Author Github: https://github.com/ludwigschuster/RasPi-GPIO-Stepmotor

    def __init__(self):
#        import time
#        import RPi.GPIO as GPIO
#        import math

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

import time
import RPi.GPIO as GPIO
import math

# /usr/share/code/project/Lucky_turntable
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

    def main(self):
        print("moving started")
        print("360 turn")
        for i in range(1): # 7
            self.turnDegrees(360)
        print("moving stopped")
        GPIO.cleanup()

###############################################################################
# main menu                                                                   #
###############################################################################

# menu item definition
# sys, GPIO, GPIO-R, Category, H/W, Class Name
menu_items = [
    [ 1, -1, -1, 'Input', 'Joystick'],
    [19, -1, -1, 'Input', '4x4 button matrix', 'ButtonMatrix'],
    [24,  0, 17, 'Input', 'Touch sensor', 'TouchSensor'],
    [26, -1, -1, 'Input', 'RC522 RFID induction module'],

    [ 2, -1, -1, 'Display', '4 Digits Segment LED', 'FourDigitSegment'],
    [ 4, -1, -1, 'Display', 'Screen driver'],
    [ 8, 25, 26, 'Display', 'GPIO indicate LED / only 26pin', 'GPIOLed'],
#    [88, 25, 26, 'Display', 'GPIO indicate LED', 'GPIOLed_DONOT_USE'],
    [12, -1, -1, 'Display', 'LCD1602', 'LCD1602'],
    [25, -1, -1, 'Display', '8x8 RGB matrix'],

    [ 9, -1, -1, 'Sensor', 'DHT11 temperature and humidity sensor', 'DHT'],
    [11,  3, 22, 'Sensor', 'Tilt sensor', 'Tilt'],
    [50, -1, 23, 'Sensor', 'Motion sensor', 'Motion'],
    [13,  4, 23, 'Sensor', 'PIR sensor'],
    [14,  5, 24, 'Sensor', 'Sound sensor', 'Sound'],
    [27, -1, -1, 'Sensor', 'Light intensity sensor', 'LightSensor'],
    [29, 27, 16, 'Sensor', 'Ultrasonic sensor', 'Ultrasonic'],

    [ 3, 29, 21, 'Other H/W', 'Relay', 'Relay'],
    [ 5, -1, -1, 'Other H/W', 'Cooling fan'],
    [ 6, -1, -1, 'Other H/W', 'Raspberry Pi and PCBA connection switch'],
    [20,  1, 18, 'Other H/W', 'Buzzer', 'Buzzer'],
    [40,  1, 18, 'Other H/W', 'Touch Button And Buzzer', 'TouchButtonAndBuzzer'],
    [21, -1, -1, 'Other H/W', 'PIR sensitivity adjustment'],
    [22,  2, 27, 'Other H/W', 'Vibration motor', 'Vibration'],
    [23, -1, -1, 'Other H/W', 'Sound sensor sensitivity adjustment'],
    [28, -1, -1, 'Other H/W', 'LCD1602 brightness adjustment'],

    [ 7, -1, -1, 'I/F', 'GPIO export'],
    [10, -1, -1, 'I/F', 'Breadboard'],
    [15, -1, -1, 'I/F', 'IR sensor interface'],
    [16, -1, -1, 'I/F', 'I/O/ADC/I2C/UART expantion interface'],
    [17, 21,  5, 'I/F', '9g servo interface', 'ServoMotor'], 
    [18, -1, -1, 'I/F', 'Stepper motor interface', 'StepMotor'],

#Camera
#Microphone

#execute pinout cmd
#Connection
#Wired LAN
#Wireless LAN
#Bluetooth
#2.4GHz Keyboard & Mouse
#USB 1/2/3/4

# storage
# df -m cmd

    [99, -1, -1, '', 'Execute ALL!', 'DUMMY'],
    [ 0, -1, -1, '', 'Exit this menu (or Ctrl+C)', 'DUMMY'],
]


def default_menu():
    import sys

    print('')
    print('CrowPi2 Sensor Tester')
    print('')
    print('   - NOT Implemented Test Function...')
    print('      G GPIO')
    print('        GR GPIO Real')

    print(' No   G GR Item')
    for item in menu_items:
        impl = '-' if len(item) == 5 else ' '
        gpio = '  ' if item[1] == -1 else str(item[1]).rjust(2, ' ')
        gpior = '  ' if item[2] == -1 else str(item[2]).rjust(2, ' ')
        # printf https://stackoverflow.com/questions/19457227/how-to-print-like-printf-in-python3/37848366#37848366
        sys.stdout.write(" %2d%s %s %s %s\n" % (item[0], impl, gpio, gpior, item[4]))
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
                # dynamic loading https://stackoverflow.com/questions/4821104/dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported-module/30941292#30941292
                import importlib
                MyClass = getattr(importlib.import_module("test_sensors"), item[5])
                instance = MyClass()
                try:
                    instance.main()
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

