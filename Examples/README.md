# Table of Contents
- [README test_sensors.py](#readme-test_sensorspy)
- [README piiio.py](#readme-piiiopy)
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

## How to execute?
~~~~
sudo python3 test_sensors.py
~~~~

+ Q. Why sudo?
+ A. RGB matrix read /dev/mem
+ Q. Why python3?
+ A. python lib 'urllib.request' for auto donwload for RFID Reader test

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
  + camera
  + mic, speaker, earphone
  + lan
  + wlan
  + bt
  + usb
  + sd card

+ command (show status)
  + lsusb, dmesg, pinout, df -h

+ Source implementation
  + refactor read-eval-print-loop
  + describe test description
  + GUI?


____

  
# README piiio.py

### What's this?
GPIO GUI Test tool using Python tkinter.


____


# A Few Tips for Developer

## Initial Setup
- Change Display Resolution
- Install VSCode

## Source Code Location
- /usr/share/code/project
  - Ref: https://github.com/Elecrow-RD/CrowPi2/issues/12

- Online Course - /usr/share/.user/course/
  - Ref: https://www.kickstarter.com/projects/elecrow/crowpi2-steam-education-platformand-raspberry-pi-laptop/comments?comment=Q29tbWVudC0zMDk1OTAwNA%3D%3D
