#!/usr/bin/env python3
import serial
import time
import req

POST_VAL = 10

def process():
    command = req.get_command() #Gets command from the Image Processing API
    print("Command: {}".format(command)) #DEBUG: Print command
    ser.write("{}\n".format(command).encode('utf-8')) #Write the command to arduino through USB Serial
    commands = ["1","2","3","4"] #Hardcoded commands
    if command in commands:
        req.post_recycled(POST_VAL);
    time.sleep(3) #Allowing time for motors

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) #Establish connection between RPI and Arduino
    time.sleep(3)
    while True:
        arduino_status = ser.readline().decode('utf-8').rstrip() #Read line from arduino
        if arduino_status == "capture":
            ser.flushInput() #Clear serial buffer to avoid chaining commands
            process() #Do the thing
