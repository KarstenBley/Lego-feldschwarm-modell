from curses import KEY_UP
from typing import Text
import keyboard
import math
import sys
from tkinter import *
import turtle

import time
import socket





def sendToSpike(s: socket, cmd: str):
    eot = b'\x04' + b'\x04' + bytes('>', 'UTF-8')

    # Send the command
    s.send(bytes(cmd, 'UTF-8') + b'\x04')
    data = bytearray()

    # Read until EOT is received
    while 1:
        tmp = s.recv(1024)
        data.extend(tmp)
        if (data.endswith(eot)):
            break

    return bytes(data[:len(data) - 3])


def getDistance(s: socket):
    data = sendToSpike(s, "print(DistanceSensorD.get_distance_cm())")
    if (data.startswith(bytes('OK', 'UTF-8')) and data.endswith(bytes('\r\n', 'UTF-8'))):
        value2 = data[2:len(data)-2]
        if value2 != b'None':
            value = int(value2)
        else:
            value = -1

        return value
    else:
        return -1


def setMotor(s: socket, speed: int):
    data = sendToSpike(s, "MotorA.start(" + str(speed) + ")")
    if (data.startswith(bytes('OK', 'UTF-8'))):
        return True
    else:
        return False


def Testrun():
    while TRUE:
        
        #connencting with lego hub
        adapter_addr = "ac:1f:0f:1d:61:c1"
        port = 1  # Normal port for rfcomm?
        buf_size = 1024

        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.connect((adapter_addr, port))

        time.sleep(0.1)
        data = s.recv(1024)
        print(data)

        s.send(b'\x03')
        time.sleep(0.1)
        s.send(b'\x01')
        data = s.recv(1024)
        print(data)

        #setting up hub
        data = sendToSpike(s, "from spike import Motor, DistanceSensor")
        print
        
        data = sendToSpike(s, "DistanceSensorD = DistanceSensor('D')")
        print(data)

        data = sendToSpike(s, "MotorA = Motor('A')")
        print(data)

        print('Test Start')
        
        while 1:
            
            distance = getDistance(s)
            if (distance != -1):
                print(distance)
            else:
                print("fehler: zu große Entfernung")
            
            
                
        text = input()
        
        #loop break
        if text == "quit":
            break
    exit()