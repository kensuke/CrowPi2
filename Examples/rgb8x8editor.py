#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import random
import threading
import time
import tkinter as tk
from tkinter import colorchooser

from rpi_ws281x import PixelStrip, Color # RGBMatrix
import spidev # ButtonMatrix
from Adafruit_LED_Backpack import SevenSegment

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
    def clear(self): print('RGBMatrixS.clear()')
    def fill(self, col): print('RGBMatrixS.fill(col='+str(col)+')')
    def dot(self, num, col): print('RGBMatrixS.dot(num='+str(num)+', col='+str(col)+')')
    def show_template(self, num, col): print('RGBMatrixS.show_template(num='+str(num)+', col='+str(col)+')')

######################################################################
# print('https://github.com/Elecrow-RD/CrowPi/tree/master/Examples/touch.py')
# Thread https://qiita.com/kotai2003/items/db7c846e0d4e2d6d6d45
class TouchSensor():

    def __init__(self, _rgb):
        self.rgb = _rgb

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
        try:
            self.started.wait()
            while self.alive:
                if self.started.is_set() == True:
                    if(GPIO.input(self.touch_pin)):
                        self.rgb.clear()
                    time.sleep(0.1)
                else:
                    self.started.wait()
                pass
        except KeyboardInterrupt: # TODO: how to interrupt?
            self.alive = False
            self.on_close()

    def on_close(self):
        self.alive = False
        if self.started.is_set() == False:
            self.started.set()
            self.thread_main.join()
        else:
            self.started.clear()
            self.started.set()

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
    def on_close(self): print('ButtonMatrixS.on_close()')

######################################################################
# global vars

root = tk.Tk()

# native
rgb = RGBMatrix()
but = ButtonMatrix(rgb)

# Skelton code for test on non-pi environment
'''
class Color():
    def __init__(self, r, g, b): pass
class SevenSegment():
    def SevenSegment(address): return SevenSegment()
    def __init__(self): self.buffer = [0, 0, 0, 0, 0, 0, 0, 0]
    def begin(self): pass
    def clear(self): pass
    def write_display(self): pass
rgb = RGBMatrixS()
but = ButtonMatrixS(rgb)
'''

touch = TouchSensor(rgb)
seg = SevenSegment.SevenSegment(address=0x70)
seg.begin()

color = tk.StringVar(value='RND')
r_var_scale = tk.IntVar()
g_var_scale = tk.IntVar()
b_var_scale = tk.IntVar()

######################################################################
# functions

# on_close: https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
def on_close():
    seg.clear()
    seg.write_display()
    touch.on_close()
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

'''
　━　　━　　　━　　━　
┃　┃┃　┃：┃　┃┃　┃
　━　　━　　　━　　━　
┃　┃┃　┃：┃　┃┃　┃
　━．　━．　　━．　━．

'''

# GUI builder
#col 0     1
# | 7 seg               | TOP
# | 8x8 | sel | color c |
# |     | rgb | scalex3 |
# |     | rnd |         |
# |     |    fill clear |
#   LEFT  RIGHT
def create_frame(frame):

# TOP for 7seg
    top = tk.Frame(frame, bd=2, relief=tk.SUNKEN)
    top.grid(row=0, column=0, columnspan=2)

    # manipulate buffer dynamically
    # https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/Adafruit_LED_Backpack/SevenSegment.py
    def set_seven_seg(pos, mask, poi = False):
        pos = pos if pos < 2 else pos-1 #  fix pos 3 -> 2, 4 -> 3 (for colon[pos=2])
        pos = 0 if pos == 0 else pos*2  # conv pos 0-0, 1-2, 2-4, 3-6
        if poi:
            seg.buffer[pos] |= (1 << 7)
        else:
            if seg.buffer[pos] & mask == 0:
                seg.buffer[pos] |= mask
            else:
                seg.buffer[pos] ^= mask
        seg.write_display()

    def show_colon():
        if seg.buffer[2] & (1 << 7) == 0:
            seg.buffer[2] |= (1 << 7) # ??
        else:
            seg.buffer[2] ^= (1 << 7) # ??
        seg.write_display()

        # official code ;-)
        #seg.buffer[4] |= 0x02
        #seg.buffer[4] &= (~0x02) & 0xFF
        #seg.write_display()

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

    dig0 = create_seg_frame(top, 0, 0)
    dig1 = create_seg_frame(top, 0, 1)
    colon = tk.Button(top, text=':', command=lambda: show_colon())
    colon.grid(row=0, column=2)
    dig2 = create_seg_frame(top, 0, 3)
    dig3 = create_seg_frame(top, 0, 4)

# LEFT
    # 8x8 button frame
    left = tk.Frame(frame, bd=2, relief=tk.SUNKEN)
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
    right = tk.Frame(frame, bd=2, relief=tk.SUNKEN)
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
    r_scale = tk.Scale(inframe2,   variable=r_var_scale, orient=tk.HORIZONTAL,   to=255)
    r_scale.grid(row=1, column=0)

    g_var_scale.set(0)
    g_scale = tk.Scale(inframe2,   variable=g_var_scale, orient=tk.HORIZONTAL,   to=255)
    g_scale.grid(row=2, column=0)

    b_var_scale.set(0)
    b_scale = tk.Scale(inframe2,   variable=b_var_scale, orient=tk.HORIZONTAL,   to=255)
    b_scale.grid(row=3, column=0)

    # R-R-3 button area
    inframe3 = tk.Frame(right, bd=1, relief=tk.SUNKEN)
    inframe3.grid(row=1, column=0, columnspan=2)

    button = tk.Button(inframe3, text='FILL', command=lambda: rgb.fill(get_color()))
    button.grid(row=0, column=0)
    button = tk.Button(inframe3, text='CLEAR', command=lambda: rgb.clear())
    button.grid(row=0, column=1)

# TODO:
# buzzer?
# vibe w
# code area
# save & load
# motor w

def main():
    root.title('CrowPi2 RGB Matrix Editor')
    root.protocol('WM_DELETE_WINDOW', on_close)

    top = tk.Frame(root, bd=2, relief=tk.SUNKEN)
#    top.grid_rowconfigure(0, weight=1)
#    top.grid_columnconfigure(0, weight=1)
#    top.pack(fill=tk.BOTH,expand=1)
    top.grid()
    create_frame(top)

    root.mainloop()

if __name__ == "__main__":
    main()
