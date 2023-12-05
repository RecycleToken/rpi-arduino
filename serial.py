#!/usr/bin/env python3
import serial
import time
import req

def process():
    command = req.getCommand()
    print("Command: {}".format(command))
    ser.write("{}\n".format(command).encode('utf-8'))
    time.sleep(3)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(3)
    while True:
        arduino_status = ser.readline().decode('utf-8').rstrip()
        if arduino_status == "capture":
            process()
