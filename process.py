#!/usr/bin/env python3
import serial
import time
import req
import queue_api as q

queue = None
recycled = {
    "plastic": 0,
    "glass": 0,
    "metal": 0,
    "paper": 0
}

def process():
    command = req.get_command() #Gets command from the Image Processing API
    # command can be plastic, glass, metal, paper, cardboard, battery
    # print("Command: {}".format(command)) #DEBUG: Print command
    commands = ["plastic", "glass", "metal", "paper", "cardboard", "battery"] #Valid commands
    if command in commands:
        if command == "cardboard":
            command = "paper"
        elif command == "battery":
            command = "metal"
        recycled[command] += 1 #Increment the recycled material
        ser.write("{}\n".format(command).encode('utf-8')) #Write the command to arduino through USB Serial
        time.sleep(2)  # wait for 2 seconds
    time.sleep(3) #Allowing time for motors

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) #Establish connection between RPI and Arduino
    time.sleep(0.2)
    while True:
        time.sleep(2) 
        queue = q.get_queue().json() #Get queue from the API

        if queue is None:
            continue

        if queue['status'] == "Terminate": #Terminate the process
            if recycled["plastic"] + recycled["glass"] + recycled["metal"] + recycled["paper"] == 0:
                q.update_queue({"status": "Failed", "user": queue['user']})
            else:
                q.create_transaction({"user": queue['user'], "recycled": recycled}) #Create transaction
            queue = None
            recycled = {
                "plastic": 0,
                "glass": 0,
                "metal": 0,
                "paper": 0
            }
            continue

        # print("Queue: {}".format(queue)) #DEBUG: Print queue
        # print("Status: {}".format(queue['status'])) #DEBUG: Print status
        if queue['status'] == "Pending":
            q.update_queue({"status": "Ready", "user": queue['user']})
        
        if queue['status'] == "Progress":
            arduino_status = ser.readline().decode('utf-8').rstrip() #Read line from arduino
            if arduino_status == "capture":
                ser.flushInput() #Flush duplicates
                process() #Do the thing
