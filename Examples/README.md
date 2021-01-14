# Table of Contents
- [README test_sensors.py](#readme-test_sensorspy)
- [README piiio.py](#readme-piiiopy)
- [README rgb8x8editor.py](#readme-rgb8x8editorpy)
- [A Few Tips for Developer](#a-few-tips-for-developer)

____

# README test_sensors.py

### What's this?
CrowPi2 sensor test program. Basically merged from CrowPi1 examples. The main purpose of this program, many sensors test on one source, no installation other packages.
+ Ref: https://www.kickstarter.com/projects/elecrow/crowpi2-steam-education-platformand-raspberry-pi-laptop/comments?comment=Q29tbWVudC0zMDgyNDA4MA%3D%3D
+ https://github.com/Elecrow-RD/CrowPi/tree/master/Examples
+ /usr/share/code/project

### Setup before execute test program
![image](https://github.com/kensuke/CrowPi2/blob/main/Examples/test_sensors.jpg)
(pic number refer from https://ksr-ugc.imgix.net/assets/029/412/859/f155bd1a92f378ed03cfb3872cf60341_original.jpg?ixlib=rb-2.1.0&auto=compress%2Cformat&q=1&w=680&fit=max&v=1591784774&frame=1&s=4f051911c4150d019b7255b3c848f259)
+ [6] Sensor Switch to "CONNECT SENSOR" left side. It's default setting.
+ [17] Connect Crowtail Moisture Sensor to SERVO port.
  + Water into Cup.
+ [17] OR Connect servo motor to SERVO port.
  + Moisture is working on connect to I2C port, but I2C port and other I2C program couldn't working same time.
+ [18] Connect step motor to STEP MOTOR port.
+ [15] Connect IR Receiver to IR Port.
  + Remote Controller.
+ [26] RFID Reader test required circle cards
  + And RFID Reader test needs MFRC522.py. If not found MFRC522.py, then automatically download, so needs internet connection.

### How to execute?
~~~~
sudo python3 test_sensors.py
~~~~

+ Q. Why sudo?
+ A. RGB matrix read /dev/mem
+ Q. Why python3?
+ A. python lib 'urllib.request' for auto donwload for RFID Reader test

~~~~
pi@raspberrypi:~/src/CrowPi2/Examples $ sudo python3 test_sensors.py 

CrowPi2 Sensor Tester

     	GP GPIO No.
     	   BC BCM No.
     	       [-] NOT Implemented Test Function...
 Cat.	GP BC No Item
 Disp	       4- Screen driver / If you seen this, screen is working (^ ^)/
 Other	       5- Cooling fan / How to control fan on software?
 I/F	       7- GPIO export
 I/F	      10- Breadboard
 I/F	    3 16- I/O/ADC/I2C/UART expantion interface
 Other	      21- PIR sensitivity adjustment
 Other	      23- Sound sensor sensitivity adjustment
 Other	      28- LCD1602 brightness adjustment
 Input	       1  Joystick
 Input	      19  4x4 button matrix
 Input	 0 17 24  Touch sensor
 Input	      26  RC522 RFID induction module / Required MFRC522.py
 Disp	       2  4 Digits Segment LED
 Disp	25 26  8  GPIO indicate LED / only 26pin
 Disp	      12  LCD1602
 Disp	      25  8x8 RGB matrix / ** Required root privileges! **
 Sensor	       9  DHT11 temperature and humidity sensor
 Sensor	 3 22 11  Tilt sensor
 Sensor	 4 23 13  PIR(Passive Infrared Ray) Motion sensor
 Sensor	 5 24 14  Sound sensor
 Sensor	      27  Light intensity sensor
 Sensor	27 16 29  Ultrasonic sensor
 Other	29 21  3  Relay
 Other	       6- Raspberry Pi and PCBA connection switch
 Other	 1 18 20  Buzzer
 Other	 1 18 40  Touch Button And Buzzer
 Other	 2 27 22  Vibration motor
 I/F	28 20 15  IR sensor interface / Remote Controller
 I/F	24 19 51  Crowtail interface / Moisture
 I/F	24 19 17  9g servo interface
 I/F	24 19 34  9g servo interface / Like a Step Motor?
 I/F	 6 25 18  Stepper motor interface
 System	      99  Execute ALL!
 System	       0  Exit this menu (or Ctrl+C)
               |
Input No       |
19         <-- Input This No

********** ********** ********** ********** <-- Test Start
[Input] - 4x4 button matrix
/usr/share/code/project/Calculator/Calculator.py
Author : original author stenobot
Original Author Github: https://github.com/stenobot/SoundMatrixPi
Press CTRL+C to exit
button 7 pressed
button 5 pressed
button 3 pressed
^Cpi@raspberrypi:~/src/CrowPi2/Examples $    <-- Ctrl+C to Exit

~~~~


### BUG?
+ LCD
~~~~
File "/usr/local/lib/python3.7/dist-packages/Adafruit_PureIO-1.1.5-py3.7.egg/Adafruit_PureIO/smbus.py", line 364, in write_i2c_block_data
TimeoutError: [Errno 110] Connection timed out

File "/usr/local/lib/python3.7/dist-packages/Adafruit_PureIO-1.1.5-py3.7.egg/Adafruit_PureIO/smbus.py", line 364, in write_i2c_block_data
OSError: [Errno 121] Remote I/O error
~~~~
reboot CrowPi2

### TODO?
+ CrowPi2 Hardware
  + switch on / off
  + gets adjuster setting value

+ Basic Hardware
  + camera / mic / speaker / earphone
  + lan / wlan / bt / 2.4GW Keyboard & Mouse
  + usb
  + sd card

+ command (show status)
  + lsusb, dmesg, pinout, df -h

+ Source implementation
  + refactor read-eval-print-loop
  + describe test description
  + GUI?
<br />
<br />
<br />

____

# README piiio.py

## 2021/1 WORKING NOW! USE CAREFULLY!!

### What's this?
GPIO GUI Test tool using Python tkinter. (I didn't use Python usually, so this and other *.py is for my Python learning project.)

### How to execute?
~~~~
python3 piiio.py
~~~~

### Python tkineter resources
+ https://tkdocs.com/tutorial/index.html
+ https://tcl.tk/man/tcl8.6/TkCmd/contents.htm
+ https://cercopes-z.com/Python/stdlib-tkinter-widget-py.html#list-widgets
+ https://docs.python.org/ja/3.7/library/tk.html
+ http://www.interq.or.jp/japan/s-imai/tcltk/tkbasic.html
<br />
<br />
<br />

____

# README rgb8x8editor.py

## 2021/1 WORKING NOW! USE CAREFULLY!!

### What's this?
RGB Matrix Editor (in first..),

1. add: 7 Seg support (I didn't planning 7 Seg implementation ^_^)
2. add: Vibration
3. add: Input Sensors - Motion, Sound, IR (remote controller), Temperature, Tilt, Ultrasonic distance, Light, Joystick and RFIDReader. almost complete.
4. add: Output Components - Buzzer, Relay, LCD, Servo Motor and Step Motor.
    1. But, I don't know 'Relay'.

become All Sensors on One App.

### How to execute?

~~~~
sudo python3 rgb8x8editor.py
~~~~

### BUG
Couldn't controll multi threads. App didn't close when clicked [x] button, try type Ctrl+C in terminal for force exit.

### TODO?
other H/W support? <s>(motor, sensors status, ...)</s> ALMOST COMPLETED roughly. Let's next step,

1. Refactor python source code (--> I'm newbie of python programming)
2. Brush up GUI (--> tkinter is a little difficult)
3. Support for Crowtail devices

<br />
<br />
<br />

____

# A Few Tips for Developer

## Initial Setup
- Change Display Resolution
  - Menu - Preferences - Appearance Settings
    - Menu Bar - Size - Large
    - System - Font - Source Code Pro? / Regular / 14?
    - Defaults - For menium screens - Set Defaults
- Change Password
  - passwd
- Disabled Crowpi2 App on Startup
- Install Visual Studio Code (for Linux .deb ARM)
  - https://code.visualstudio.com/download

### For Japanese
~~~~
sudo apt install ibus
sudo apt install ibus-mozc
reboot
~~~~

## Source Code Location
- /usr/share/code/project
  - Ref: https://github.com/Elecrow-RD/CrowPi2/issues/12

- Online Course - /usr/share/.user/course/
  - Ref: https://www.kickstarter.com/projects/elecrow/crowpi2-steam-education-platformand-raspberry-pi-laptop/comments?comment=Q29tbWVudC0zMDk1OTAwNA%3D%3D
