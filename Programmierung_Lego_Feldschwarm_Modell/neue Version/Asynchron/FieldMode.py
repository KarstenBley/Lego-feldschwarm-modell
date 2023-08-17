from curses import KEY_UP
from tkinter import Y
import keyboard
import math
import sys
from tkinter import *
import turtle
import threading
import time
import socket

Abstand = 0
speed = 0
Steeringangle = 0
positionX = 400
positionY = 400
Heading = 90
broken = False
Attachment_up = True
def stop():
    global running
    running = False


def sendToSpike(s: socket, cmd: str):
    eot = b'\x04' + b'\x04' + bytes('>', 'UTF-8')
    neot = b'\r\n' + b'\x04' + bytes('>', 'UTF-8')
    # Send the command
    s.send(bytes(cmd, 'UTF-8') + b'\x04')
    data = bytearray()

    # Read until EOT is received
    while 1:
        tmp = s.recv(1024)
        data.extend(tmp)
        if (data.endswith(eot)):
            break
        elif(data.endswith(neot)):
            print("Systemfehler, überprüfen Sie die Rechtschreibung der Befehle")
            exit()

    return bytes(data[:len(data) - 3])


def getDistance(s: socket):
    data = sendToSpike(s, "print(DistanceSensorD.get_distance_cm())")
    if (data.startswith(bytes('OK', 'UTF-8')) and data.endswith(bytes('\r\n', 'UTF-8'))):
        value = data[2:len(data) - 2]
        if value != b'None':
            value = int(value)
        else:
            value = -1
        return value
    else:
        return -2
   
def getSensorData(s: socket):
    data = sendToSpike(s, "getSensorData()")
    if (data.startswith(bytes('OK', 'UTF-8')) and data.endswith(bytes('\r\n', 'UTF-8'))):
        valuesStr = data[2:len(data) - 2]
        values = valuesStr.split(b',')
        return list(map(lambda x: int(x) if x != b'None' else -1, values))
    else:
        return list()
    

def sendwithtest(s: socket, cmd):
    data = sendToSpike(s, cmd)
    distancetest = getDistance(s)
    while distancetest <= 5:
        print("blockiert")
        distancetest = getDistance(s)

def Autopilot(s: socket, rota = None, TargetHeading = None, direction = None, stayStraight = False, destinationY = None, destinationX = None):
    print("started")
    global Abstand
    global rotations
    global speed
    global Steeringangle
    global Heading
    Abstand = 0
    speed = 0
    Steeringangle = 0
    rotations = 0
    r = 0
    data = sendToSpike(s, "AccelerationB.set_degrees_counted(0)")
    while True:
        if rota != None:
            if rota < 0:
                data = sendToSpike(s, "AccelerationB.start(75)")
                r = -1
            elif rota > 0:
                data = sendToSpike(s, "AccelerationB.start(-75)")
                r = -1
        elif direction == 1:
            data = sendToSpike(s, "AccelerationB.start(-75)")
            r = -1
        elif direction == -1:
            data = sendToSpike(s, "AccelerationB.start(75)")
            r = -1
        #

        values = getSensorData(s)
        if (len(values) == 4):
            Abstand = values[0]
            speed = values[1]
            Steeringangle = values[2]
            rotations = values[3]
            rotations = rotations / 360 * r
        if speed > 0:
            Heading += Steeringangle * speed / 2000
        elif speed < 0:
            Heading += Steeringangle * speed*-1 / 2000
        distancetest = Abstand
        if Heading <= 0:
            Heading = 360 + (Heading % 360)
        else:
            Heading = Heading % 360

        if Heading > 180 and destinationX != None:
            if destinationX > positionX:
                data = sendToSpike(s, "AccelerationB.stop()")
                values = getSensorData(s)
                speed = 0
                print("ended")
                break
        elif Heading < 180 and destinationX != None:
            if destinationX < positionX:
                data = sendToSpike(s, "AccelerationB.stop()")
                values = getSensorData(s)
                speed = 0
                print("ended")
                break

        while distancetest <= 5 and distancetest >= 0:
            print("blockiert")
            speed = 0
            data = sendToSpike(s, "AccelerationB.stop()")
            distancetest = getDistance(s)
        #
        if rota != None:
            if rotations > rota and rotations > 0:
                data = sendToSpike(s, "AccelerationB.stop()")
                values = getSensorData(s)
                speed = 0
                print("ended")
                break
            elif rotations < rota and rotations < 0:
                data = sendToSpike(s, "AccelerationB.stop()")
                values = getSensorData(s)
                speed = 0
                print("ended")
                break
        if TargetHeading == 360:
           if Heading > 358:
                data = sendToSpike(s, "AccelerationB.stop()")
                values = getSensorData(s)
                speed = 0
                break
        elif Steeringangle > 0 and TargetHeading != None and direction == -1:
            if Heading <= TargetHeading and Heading > TargetHeading - 1:
                data = sendToSpike(s, "AccelerationB.stop()")
                values = getSensorData(s)
                speed = 0
                break
        elif Steeringangle < 0 and TargetHeading != None and direction == -1:
            if Heading >= TargetHeading and Heading < TargetHeading +1:
                data = sendToSpike(s, "AccelerationB.stop()")
                values = getSensorData(s)
                speed = 0
                break
        elif Steeringangle < 0 and TargetHeading != None and direction == 1:
            if Heading <= TargetHeading and Heading > TargetHeading -1:
                data = sendToSpike(s, "AccelerationB.stop()")
                values = getSensorData(s)
                speed = 0
                break
        elif Steeringangle > 0 and TargetHeading != None and direction == 1:
            if Heading >= TargetHeading and Heading < TargetHeading + 1:
                data = sendToSpike(s, "AccelerationB.stop()")
                values = getSensorData(s)
                speed = 0
                break
        if stayStraight:
            Steeringangle = getAngle(s)
            if Steeringangle != 0:
                sendToSpike(s, "SteeringE.run_for_degrees("+str(Steeringangle*-1)+")")
                print("straightening")
                print(getAngle(s))
        if Heading > 180 and destinationY != None:
            Steeringangle = getAngle(s)
            if positionY > destinationY and Steeringangle < 2:
                print("left")
                sendToSpike(s, "SteeringE.run_for_degrees(10)")
            if positionY < destinationY and Steeringangle > -2:
                print("right")
                sendToSpike(s, "SteeringE.run_for_degrees(-10)")
            print(Steeringangle)

        elif Heading < 180 and destinationY != None:
            Steeringangle = getAngle(s)
            if positionY < destinationY and Steeringangle < 2:
                print("left")
                sendToSpike(s, "SteeringE.run_for_degrees(10)")
            if positionY > destinationY and Steeringangle > -2:
                print("right")
                sendToSpike(s, "SteeringE.run_for_degrees(-10)")
            print(Steeringangle)
        



def isStalled(s: socket):
    global valueStalled2
    dataStalled = sendToSpike(s, "print(SteeringE.was_stalled())")
    if (dataStalled.startswith(bytes('OK', 'UTF-8')) and dataStalled.endswith(bytes('\r\n', 'UTF-8'))):
        valueStalled2 = dataStalled[2:len(dataStalled) - 2]
        if valueStalled2.startswith(bytes('True', 'UTF-8')):
            return True
    return False

def getAngle(s: socket):
    global valueAngle2
    dataAngle = sendToSpike(s, "print(SteeringE.get_degrees_counted())")
    if (dataAngle.startswith(bytes('OK', 'UTF-8'))
            and dataAngle.endswith(bytes('\r\n', 'UTF-8'))):
        valueAngle2 = dataAngle[2:len(dataAngle) - 2]
        if valueAngle2 != b'None' and not valueAngle2.startswith(
                bytes('OK', 'UTF-8')):
            valueAngle = int(valueAngle2)
        else:
            valueAngle = "Error"

        return valueAngle

def runfieldmode(y,b,anz):
    print(b)
    global Attachment_up
    global Heading
    global positionX
    destinationX = 0
    a = 0
    x = 0
    bnz = 0
   
    #connecting with lego hub
    #first hub: ac:1f:0f:1d:61:c1
    #second hub: 64:8c:bb:08:8f:24
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
    print(data)

    data = sendToSpike(s, "AccelerationB = Motor('B')")
    print(data)

    data = sendToSpike(s, "SteeringE = Motor('E')")
    print(data)

    data = sendToSpike(s, "Chassis = Motor('C')")
    print(data)

    data = sendToSpike(s, "Attachment = Motor('A')")
    print(data)

    data = sendToSpike(s, "DistanceSensorD = DistanceSensor('D')")
    print(data)

    data = sendToSpike(s, "SteeringE.set_stall_detection(True)")
    print(data)

    data = sendToSpike(s, "SteeringE.set_stop_action('hold')")
    print(data)

    data = sendToSpike(s, "hub.display.show('hello')")
    print(data)

    data = sendToSpike(s, "DistanceSensorD.light_up_all(100)")
    print(data)

    data = sendToSpike(s,"def getSensorData():\r\n    print(str(DistanceSensorD.get_distance_cm()) + ',' + str(AccelerationB.get_speed()*-1) + ',' + str(int(SteeringE.get_degrees_counted()/2)) + ',' + str(int(AccelerationB.get_degrees_counted())))")
    print(data)
    while not isStalled(s):
        sendToSpike(s, "SteeringE.run_for_degrees(100)")
    sendToSpike(s, "SteeringE.run_for_degrees(-50)")
    sendToSpike(s, "SteeringE.set_degrees_counted(0)")
    sendToSpike(s, "Chassis.run_for_rotations(5)")

    sendToSpike(s, "Attachment.run_for_rotations(2)")
    Attachment_up = False
    while a < b:
      
        #lower chassis and attachment

        Autopilot(s,y * 3, destinationY = positionY)
        destinationX = positionX
        
        if (a % 2) == 0 and a < b-1:
            
            #turn right
            sendToSpike(s, "Attachment.run_for_rotations(-2)")
            Attachment_up = True
            #
            sendToSpike(s, "SteeringE.run_for_degrees(-35)")
            #
            f = 0
            Autopilot(s,TargetHeading = 360, direction = 1)
            #
            sendToSpike(s, "SteeringE.run_for_degrees(35)")
            #
            while bnz < anz:
                Autopilot(s,-3, stayStraight = True)
                print(data)
                bnz = bnz + 1
            
            bnz = 0
            #
            sendToSpike(s, "SteeringE.run_for_degrees(-35)")
            #
            f = 0
            Autopilot(s,TargetHeading = 270, direction = -1)
            #
            sendToSpike(s, "SteeringE.run_for_degrees(35)")
            f = 0
            
            Autopilot(s, destinationX = destinationX, direction = 1, destinationY = positionY)
            #
            sendToSpike(s, "Attachment.run_for_rotations(2)")
            Attachment_up = False
            
            x = 0
            #print(a,b)
            print("wenden1")
        elif  (a % 2) == 1 and a < b-1:
            
            #turn left
            sendToSpike(s, "Attachment.run_for_rotations(-2)")
            Attachment_up = True
            #
            sendToSpike(s, "SteeringE.run_for_degrees(35)")
            #
            f = 0
            Autopilot(s,TargetHeading = 360, direction = 1)
            #            
            sendToSpike(s, "SteeringE.run_for_degrees(-35)")
            #
            while bnz < anz:
                Autopilot(s,-3, stayStraight = True)
                print(data)
                bnz = bnz + 1
            
            bnz = 0
            #
            sendToSpike(s, "SteeringE.run_for_degrees(35)")
            #
            f = 0
            Autopilot(s,TargetHeading = 90, direction = -1)
            #
            sendToSpike(s, "SteeringE.run_for_degrees(-35)")
            #
            f = 0

            Autopilot(s, destinationX = destinationX, direction = 1, destinationY = positionY)
            #
            sendToSpike(s, "Attachment.run_for_rotations(2)")
            Attachment_up = False
            
            
            x = 0
            print("wenden2")
        a = a + 1
        print(a)
      
        #raise attachment and chassis
    sendToSpike(s, "Chassis.run_for_rotations(-5)")

    sendToSpike(s, "Attachment.run_for_rotations(-2)")
    exit()