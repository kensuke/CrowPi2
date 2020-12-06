# README test_sensors.py

### What's this?
CrowPi2 sensor test program. Basically merged from CrowPi1 examples.

The main purpose of this program, many sensors test on one source, no installation other packages.
+ https://github.com/Elecrow-RD/CrowPi/tree/master/Examples
+ /usr/share/code/project

### Setup before execute test program
+ Sensor Switch to "CONNECT SENSOR" left side. It's default setting.
+ Connect Crowtail Moisture Sensor to SERVO port.
++ Water into Cup.
+ OR Connect servo motor to SERVO port.
++ Moisture is working on connect to I2C port, but I2C port and other I2C program couldn't working same time.
+ Connect step motor to STEP MOTOR port.
+ Connect IR Receiver to IR Port.
++ Remote Controller.
+ RFID Reader test required circle cards
++ And RFID Reader test needs MFRC522.py. If not found MFRC522.py, then automatically download, so needs internet connection.

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
++ switch on / off
++ gets adjuster setting value

+ Basic Hardware
++ camera
++ mic, speaker, earphone
++ lan
++ wlan
++ bt
++ usb
++ sd card

+ command (show status)
++ lsusb, dmesg, pinout, df -h

+ Source implementation
++ refactor read-eval-print-loop
++ describe test description
++ GUI?
