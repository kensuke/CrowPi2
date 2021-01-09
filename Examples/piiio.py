#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkfont
#import tkinter.tix as tix # for balloon (as tooltip) # needs py3.9...
import RPi.GPIO as GPIO

'''
def check_const(name, defval, realval):
    print(name + '\t' + str(defval) + '\t' + str(realval) + '\t' + str(defval == realval))

check_const('HIGH', 1, GPIO.HIGH)
check_const('LOW', 0, GPIO.LOW)
check_const('IN', 1, GPIO.IN)
check_const('OUT', 0, GPIO.OUT)

check_const('SERIAL', 40, GPIO.SERIAL)
check_const('SPI', 41, GPIO.SPI)
check_const('I2C', 42, GPIO.I2C)
check_const('PWM', 43, GPIO.PWM)
check_const('HARD_PWM', 43, GPIO.HARD_PWM)

#print(GPIO.MODE_UNKNOWN)
check_const('UNKNOWN', -1, GPIO.UNKNOWN)
check_const('BOARD', 10, GPIO.BOARD)
check_const('BCM', 11, GPIO.BCM)

check_const('PUD_OFF', 20, GPIO.PUD_OFF)
check_const('PUD_DOWN', 21, GPIO.PUD_DOWN)
check_const('PUD_UP', 22, GPIO.PUD_UP)

check_const('RISING', 31, GPIO.RISING)
check_const('FALLING', 32, GPIO.FALLING)
check_const('BOTH', 33, GPIO.BOTH)
'''

################################################################################
# DATA Definition                                                              #
################################################################################

mode_table = {
    -2:           'PWR', # POWER # -2 local definition
    GPIO.UNKNOWN: 'UNK',         # -1 official definition
    GPIO.IN:      'IN',          #  1
    GPIO.OUT:     'OUT',         #  0
    GPIO.SERIAL:  'SER',         # 40
    GPIO.SPI:     'SPI',         # 41
    GPIO.I2C:     'I2C',         # 42
    GPIO.HARD_PWM:'PWM'          # 43
}

gpio_pins = [
    # PHYSICAL Port No / GPIO No. / BCM No. / Description / IO -2-disabled, 0-Input, 1-Output
    #PHY GP  BCM  DESC       IO           PHY GP  BCM  DESC      IO           # Always ON
    [ 1, -1, -1, '3V3',            -2],  [ 2, -1, -1, '5V',            -2],   # * *
    [ 3, -1,  2, 'SDA1',     GPIO.I2C],  [ 4, -1, -1, '5V',            -2],   #   *
    [ 5, -1,  3, 'SCL1',     GPIO.I2C],  [ 6, -1, -1, 'GND',           -2],   #
#    [ 7,  7,  4, '1Wire',    GPIO.OUT],  [ 8, -1, 14, 'TxD', GPIO.MODE_UNKNOWN],
#    [ 9, -1, -1, 'GND',            -2],  [10, -1, 15, 'RxD', GPIO.MODE_UNKNOWN],
    [ 7,  7,  4, '1Wire',    GPIO.OUT],  [ 8, -1, 14, 'TxD', -1],
    [ 9, -1, -1, 'GND',            -2],  [10, -1, 15, 'RxD', -1],
    [11,  0, 17, 'Touch',     GPIO.IN],  [12,  1, 18, 'Buzzer',  GPIO.OUT],
    [13,  2, 27, 'Vibration',GPIO.OUT],  [14, -1, -1, 'GND',           -2],
    [15,  3, 22, 'Tilt',      GPIO.IN],  [16,  4, 23, 'Motion',   GPIO.IN],   # * *blink
    [17, -1, -1, '3V3',            -2],  [18,  5, 24, 'Sound',    GPIO.IN],   # *
    [19, -1, 10, 'MOSI',     GPIO.SPI],  [20, -1, -1, 'GND',           -2],
    [21, -1,  9, 'MISO',     GPIO.SPI],  [22,  6, 25, 'Step-M-4',GPIO.OUT],
    [23, -1, 11, 'SCLK',     GPIO.SPI],  [24, -1,  8, 'CE0',      GPIO.IN],
    [25, -1, -1, 'GND',            -2],  [26, -1,  7, 'CE1',      GPIO.IN],
    [27, -1,  0, 'SDA0',           -2],  [28, -1,  1, 'SCL0',          -2],   # *
    [29, 21,  5, 'Step-M-1', GPIO.OUT],  [30, -1, -1, 'GND',           -2],
    [31, 22,  6, 'Step-M-2', GPIO.OUT],  [32, 26, 12, 'RGB Matrix?', GPIO.OUT],
    [33, 23, 13, 'Step-M-3', GPIO.OUT],  [34, -1, -1, 'GND',           -2],
    [35, 24, 19, 'Servo-M',  GPIO.OUT],  [36, 27, 16, 'Uls-TRIG',GPIO.OUT],
    [37, 25, 26, 'Uls-ECHO',  GPIO.IN],  [38, 28, 20, 'IR',       GPIO.IN],
    [39, -1, -1, 'GND',            -2],  [40, 29, 21, 'Relay',   GPIO.OUT],
]

# open / close
#   in
#      input()
#   out
#      high or low

def create_frame(parent, pin):
    upper = True if pin[0] % 2 == 1 else False
    disabled = True if pin[4] == -2 else False

    frame = tk.Frame(parent, bd=1, relief=tk.SUNKEN)
#       col= 0  1 ... 18 19
# row=0     39 37 ...  3  1 # upper
# row=1     40 38 ...  4  2
    frame.grid(row=0 if upper else 1, column=int((40 - (pin[0] + (1 if upper else 0))) / 2))

# top-frame-row=0 # upper
#   inner-row=0 Description       label
#             1 BCM No.           label
#             2 UP    HIGH   inframe  outframe
#               DOWN  LOW
#             3 IN    OUT         ioframe
#             4 Mode Str          label
#             5 Button            butframe
#             6 PYH No.           label
# - - - - - - -  - - - - mirror
# top-frame-row=1
#   inner-row=0 PYH No.
#             1 Button
#             2 Mode Str
#             3 IN    OUT
#             4 UP    HIGH
#               DOWN  LOW
#             5 BCM No.
#             6 Description

    label_desc = tk.Label(frame, text=pin[3])
    label_desc.grid(row=0 if upper else 6, column=0, columnspan=2)            #*** inner-row
    label_bcm = tk.Label(frame, text=pin[2])
    label_bcm.grid( row=1 if upper else 5, column=0, columnspan=2)            #*** inner-row

    label_mode = tk.Label(frame, text=mode_table[pin[4]])
    label_mode.grid(row=4 if upper else 2, column=0, columnspan=2)            #*** inner-row

    label_phy = tk.Label(frame, text=str(pin[0]))
    label_phy.grid( row=6 if upper else 0, column=0, columnspan=2)            #*** inner-row

# input PULL_UP or DOWN # TODO: NONE?
    inframe = tk.Frame(frame, bd=1, relief=tk.SUNKEN)
    inframe.grid(   row=2 if upper else 4, column=0, sticky=tk.E)             #*** inner-row

    in_pud = tk.StringVar(value='NONE')
    in_pud_up   = tk.Radiobutton(inframe, text='', variable=in_pud, value='UP')
    in_pud_none   = tk.Radiobutton(inframe, text='', variable=in_pud, value='NONE')
    in_pud_down = tk.Radiobutton(inframe, text='', variable=in_pud, value='DOWN')
    in_pud_up.grid(row=0, column=0)
    in_pud_none.grid(row=1, column=0)
    in_pud_down.grid(row=2, column=0)

# output HIGH or LOW
    out_hl = tk.StringVar(value='LOW')

    def high_low_selected(event):
        print('GPIO.output('+str(pin[2])+', '+out_hl.get()+') # ' + pin[3])
        GPIO.output(pin[2], GPIO.LOW if out_hl.get() == 'LOW' else GPIO.HIGH)

    outframe = tk.Frame(frame, bd=1, relief=tk.SUNKEN)
    outframe.grid(  row=2 if upper else 4, column=1, sticky=tk.W)             #*** inner-row

    out_high = tk.Radiobutton(outframe, text='', variable=out_hl, value='HIGH')
    out_low  = tk.Radiobutton(outframe, text='', variable=out_hl, value='LOW')
    out_high.bind("<ButtonPress-1>", high_low_selected)
    out_low.bind("<ButtonPress-1>", high_low_selected)
    out_high.grid(row=0, column=0)
    out_low.grid(row=1, column=0)

# input or output
    ioframe = tk.Frame(frame, bd=1, relief=tk.SUNKEN)
    ioframe.grid(   row=3 if upper else 3, column=0, columnspan=2)            #*** inner-row

#GPIO.IN, GPIO.OUT, GPIO.SPI, GPIO.I2C, GPIO.HARD_PWM, GPIO.SERIAL, GPIO.UNKNOWN
    inout = tk.StringVar(value='IN' if pin[4] == GPIO.IN else 'OUT')
    inout_in  = tk.Radiobutton(ioframe, text='', variable=inout, value='IN')
    inout_out = tk.Radiobutton(ioframe, text='', variable=inout, value='OUT')
    inout_in.grid(row=0, column=0)
    inout_out.grid(row=0, column=1)

# vertical button: https://stackoverflow.com/questions/38008389/is-it-possible-to-have-a-vertical-oriented-button-in-tkinter
    def button_pressed(event):
        #print('button['+str(pin[0])+'] inout['+inout.get()+'] in['+in_pud.get()+'] out['+out_hl.get()+']')
        #print(pin)

        # open or close
        GPIO.setmode(GPIO.BCM)
        if inout.get() == 'IN':
            GPIO.setup(pin[2], GPIO.IN, pull_up_down=GPIO.PUD_UP if in_pud.get() == 'UP' else GPIO.PUD_DOWN)
            val = GPIO.input(pin[2])
            print(val)
        else:
            GPIO.setup(pin[2], GPIO.OUT)

    butframe = tk.Frame(frame, bd=0, relief=tk.SUNKEN)
    butframe.grid(  row=5 if upper else 1, column=0, columnspan=2)            #*** inner-row

    but_label = pin[3] if pin[1] == -1 else 'IO'+str(pin[1])
    font = tkfont.nametofont("TkDefaultFont")
    height = 35 #font.measure(but_label) + 4 # set static size
    width = font.metrics()['linespace'] + 4

# raised, sunken, flat, ridge, solid, and groove
    canvas = tk.Canvas(butframe, height=height, width=width, borderwidth=2, relief='ridge' if disabled else 'raised')
    canvas.create_text((4, 4), angle="270", anchor="sw", text=but_label, font=font)
    canvas.state = tk.NORMAL if pin[4] != -1 else tk.DISABLED
#    if not disabled:
    canvas.bind("<ButtonPress-1>", button_pressed)#lambda ev: ev.widget.configure(relief="sunken"))
    canvas.grid()

    # tooltip: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter/61879204#61879204
    #balloon = tix.Balloon(parent, bg="white", title="Help")
    #balloon.bind_widget(frame, balloonmsg=pin[3] + '\ninout['+inout.get()+']\nin['+in_pud.get()+']\nout['+out_hl.get()+']')

    return frame


# tix error: https://stackoverflow.com/questions/52001532/python-3-7-tkinter-tclerror-invalid-command-name-tixballoon/52001957#52001957
root = tk.Tk()
#root = tix.Tk()

# on_close: https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
def on_close():
    GPIO.cleanup()
    root.destroy()

# https://sourceforge.net/p/raspberry-gpio-python/wiki/Checking%20function%20of%20GPIO%20channels/
def detect_pin_function():
    GPIO.setmode(GPIO.BOARD)
    for pi in range(40):
        pin = gpio_pins[pi]
        if pin[3] == '3V3' or pin[3] == '5V' or pin[3] == 'GND' or pin[3] == 'SDA0' or pin[3] == 'SCL0':
            print('pin['+str(pin[0])+'] = [' + mode_table[-2] + '](-2)')
            gpio_pins[pi][4] = -2
            continue
        func = GPIO.gpio_function(pin[0])
        if func != gpio_pins[pi][4]:
            print('definition mismatch! pin['+str(pin[0])+'] static['+mode_table[gpio_pins[pi][4]]+']('+str(gpio_pins[pi][4])+') dynamic['+mode_table[func]+']('+str(func)+')')
        gpio_pins[pi][4] = func
        print('pin['+str(pin[0])+'] = [' + mode_table[func] + ']('+str(func)+')')
    GPIO.cleanup() # for GPIO.setmode(GPIO.BCM)

def main():
    #detect_pin_function()
    root.title('CrowPi2 GPIO Tester')
    root.protocol('WM_DELETE_WINDOW', on_close)

    top = tk.Frame(root, bd=2, relief=tk.SUNKEN)
#    top.grid_rowconfigure(0, weight=1)
#    top.grid_columnconfigure(0, weight=1)
#    top.pack(fill=tk.BOTH,expand=1)
    top.grid()

    for pin in gpio_pins:
        if pin[0] % 2 == 1: # upper
            f = create_frame(top, pin)

    for pin in gpio_pins:
        if pin[0] % 2 == 0:
            f = create_frame(top, pin)

    root.mainloop()


if __name__ == "__main__":
    main()
