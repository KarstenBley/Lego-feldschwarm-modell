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


def getForce(s: socket):
    data = sendToSpike(s, "print(ForcesensorB.get_force_newton())")
    if (data.startswith(bytes('OK', 'UTF-8')) and data.endswith(bytes('\r\n', 'UTF-8'))):
        value = int(data[2:len(data)-2])
        return value
    else:
        return -1

    
def getDistance(s: socket):
    data = sendToSpike(s, "print(DistanceSensorD.get_distance_cm())")
    if (data.startswith(bytes('OK', 'UTF-8')) and data.endswith(bytes('\r\n', 'UTF-8'))):
        value = int(data[2:len(data)-2])
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
        data = sendToSpike(s, "from spike import Motor, DistanceSensor, ForceSensor")
        print(data)

        
        s.send(bytes("AccelerationB = Motor('B')", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("DistancesensorD = DistanceSensor('D')", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("SteeringE = Motor('E')", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("Chassis = Motor('C')", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("Attachment = Motor('A')", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("SteeringE.set_stall_detection(True)", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("Chassis.set_stall_detection(True)", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("SteeringE.set_degrees_counted(0)", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("Chassis.set_degrees_counted(0)", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("Attachment.set_degrees_counted(0)", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("AccelerationB.set_degrees_counted(0)", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)                  

        s.send(bytes("SteeringE.set_stop_action('hold')", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("hub.display.show('hello')", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

        s.send(bytes("DistancesensorD.light_up_all(100)", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)


        print('Test Start')
        
        while 1:
            #force = getForce(s)
            distance = getDistance(s)
            if (distance != -1):
                print(distance)
        
        text = input()
        
        #loop break
        if text == "quit":
            break
    exit()