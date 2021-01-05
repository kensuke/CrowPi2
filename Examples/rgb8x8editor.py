
import tkinter as tk
import RPi.GPIO as GPIO

######################################################################
# LED matrix
from rpi_ws281x import PixelStrip, Color
import random
import time
class RGBMatrix:

    def __init__(self):
#        print('/usr/share/code/project/Tilt_reminder/Tilt_reminder.py')

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
            [7, 6, 5, 4, 3, 2, 1, 9, 17, 25, 33, 34, 35, 36, 37, 38, 39, 31, 23, 15, 47, 55, 63, 62, 61, 60, 59, 58, 57] # 9
        ]

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def on_close(self):
        self.colorWipe(Color(0,0,0), 10)

    def show_number(self, num):
        self.colorWipe(Color(0,0,0), 10)
        r, g, b = random.randint(10, 250), random.randint(10, 250), random.randint(10, 250)
        for cell in self.numbers[int(num)]:
            self.strip.setPixelColor(cell, Color(r, g, b))
        self.strip.show()

    def dot(self, num):
        r, g, b = random.randint(10, 250), random.randint(10, 250), random.randint(10, 250)
        self.strip.setPixelColor(int(num), Color(r, g, b))
        self.strip.show()

root = tk.Tk()
rgb = RGBMatrix()

# on_close: https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
def on_close():
    rgb.on_close()
    GPIO.cleanup()
    root.destroy()

def on_button_pressed(id):
#    rgb.show_number(id)
    rgb.dot(id)

def create_button(top, x, y):
    pos = y * 8 + x
    button = tk.Button(top, text=' ', command=lambda: on_button_pressed(str(pos)))
    button.grid(row=y, column=x)

def main():
    root.title('CrowPi2 GPIO Tester')
    root.protocol('WM_DELETE_WINDOW', on_close)

    top = tk.Frame(root, bd=2, relief=tk.SUNKEN)
#    top.grid_rowconfigure(0, weight=1)
#    top.grid_columnconfigure(0, weight=1)
#    top.pack(fill=tk.BOTH,expand=1)
    top.grid()

    for y in range(0, 8):
        for x in range(0, 8):
            create_button(top, x, y)

    root.mainloop()

if __name__ == "__main__":
    main()
