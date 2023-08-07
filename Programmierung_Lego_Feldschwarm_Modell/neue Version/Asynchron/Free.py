from curses import KEY_UP
from typing import Text
import keyboard
import math
import sys
from tkinter import *
import turtle
import tkinter as tk
import asyncio

import time
import socket

PositionA = int
speedB = int
PositionC = int
angleE = int
distanceD = float
running = bool
running = True


class Spike:
    def __init__(self, adapter_addr, port):
        self.isOpen = False
        self.isSending = False
        self.s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.adapter_addr = adapter_addr
        self.port = port 

        # State variables       
        self.Abstand = -1
        self.Test = -1
        self.Speed = 0
        self.SteeringAngle = 0
        self.SpeedReq = 0
        self.SteeringAngleReq = 0
        self.Chassisheight = 0
        self.Chassisheightreq = 0
        self.Attmheight = 0
        self.Attmheightreq = 0
        
    def connect(self):
        self.s.connect((self.adapter_addr, self.port))

        time.sleep(0.1)
        data = self.s.recv(1024)
        print(data)

        self.s.send(b'\x03')
        time.sleep(0.1)
        self.s.send(b'\x01')
        time.sleep(0.5)
        data = self.s.recv(1024)
        print(data)

        print(data)

        self.isOpen = True

        #setting up hub
        data = self.sendToSpike("from spike import Motor, DistanceSensor")
        print(data)

        data = self.sendToSpike("AccelerationB = Motor('B')")
        print(data)

        data = self.sendToSpike("DistanceSensorD = DistanceSensor('D')")
        print(data)

        data = self.sendToSpike("SteeringE = Motor('E')")
        print(data)

        data = self.sendToSpike("Chassis = Motor('C')")
        print(data)

        data = self.sendToSpike("Attachment = Motor('A')")
        print(data)

        data = self.sendToSpike("SteeringE.set_stall_detection(True)")
        print(data)

        data = self.sendToSpike("Chassis.set_stall_detection(True)")
        print(data)

        data = self.sendToSpike("SteeringE.set_degrees_counted(0)")
        print(data)

        data = self.sendToSpike("Chassis.set_degrees_counted(0)")
        print(data)

        data = self.sendToSpike("Attachment.set_degrees_counted(0)")
        print(data)

        data = self.sendToSpike("AccelerationB.set_degrees_counted(0)")
        print(data)                  

        data = self.sendToSpike("SteeringE.set_stop_action('hold')")
        print(data)

        data = self.sendToSpike("hub.display.show('hello')")
        print(data)

        data = self.sendToSpike("DistanceSensorD.light_up_all(100)")
        print(data)

        data = self.sendToSpike("def getSensorData():\r\n    print(str(DistanceSensorD.get_distance_cm()) + ',' + str(AccelerationB.get_speed()*-1) + ',' + str(int(SteeringE.get_degrees_counted()/2)))")
        print(data)

    def close(self):    
        if (self.isOpen):
            self.s.close()
        self.isOpen = False

    def sendToSpike(self, cmd: str):
        if (not self.isOpen or self.isSending):
            return bytes('None\r\n', 'UTF-8')
        self.isSending = True

        eot = b'\x04' + b'\x04' + bytes('>', 'UTF-8')

        # sendToSpike the command
        self.s.send(bytes(cmd, 'UTF-8') + b'\x04')
        time.sleep(0.1)
        data = bytearray()

        # Read until EOT is received
        while 1:
            try:
                tmp = self.s.recv(1024)
                time.sleep(0.1)
                data.extend(tmp)
                if (data.endswith(eot)):
                    break
            except:
                print(data)
                break

        self.isSending = False
        return bytes(data[:len(data) -3])    

    def getDistance(self):
        data = self.sendToSpike("print(DistanceSensorD.get_distance_cm())")
        if (data.startswith(bytes('OK', 'UTF-8')) and data.endswith(bytes('\r\n', 'UTF-8'))):
            value2 = data[2:len(data)-2]
            if value2 != b'None':
                value = int(value2)
            else:
                value = -1
            return value
        else:
            return -2
        
    def getSensorData(self):
        data = self.sendToSpike("getSensorData()")
        if (data.startswith(bytes('OK', 'UTF-8')) and data.endswith(bytes('\r\n', 'UTF-8'))):
            valuesStr = data[2:len(data)-2]
            values = valuesStr.split(b',')
            return list(map(lambda x: int(x) if x != b'None' else -1, values))
        else:
            return list()
        
    def move(self, speed: int):
        self.SpeedReq = speed

    def steer(self, angle: int):
        self.SteeringAngleReq = angle
        
    def Chassish(self, cheight: int):
        self.Chassisheightreq = cheight

    def Attachmentheight(self, aheight: int):
        self.Attmheightreq = aheight

    def update(self):
        # Model update
        # self.Abstand = self.getDistance()
        values = self.getSensorData()
        if (len(values) == 3):
            self.Abstand = values[0]
            self.Test = values[1]
            self.Steeringangle = values[2]

        # -update speed and angle, if requested
        if self.Speed != self.SpeedReq:
            self.Speed = self.SpeedReq
            if self.Speed != 0:
                self.sendToSpike("AccelerationB.start(" + str(self.Speed) + ")")
            else:
                self.sendToSpike("AccelerationB.stop()")
        
        if self.SteeringAngle != self.SteeringAngleReq:
            self.SteeringAngle = self.SteeringAngleReq
            if self.SteeringAngle != 0:
                self.sendToSpike("SteeringE.start(" + str(self.SteeringAngle) + ")")
            else:
                self.sendToSpike("SteeringE.stop()")

        if self.Chassisheight != self.Chassisheightreq:
            self.Chassisheight = self.Chassisheightreq
            if self.Chassisheight == -1:
                self.sendToSpike("Chassis.run_for_rotations(5)")
            elif self.Chassisheight == 1:
                self.sendToSpike("Chassis.run_for_rotations(-5)")

        if self.Attmheight != self.Attmheightreq:
            self.Attmheight = self.Attmheightreq
            if self.Attmheight == -1:
                self.sendToSpike("Attachment.run_for_rotations(2)")
            elif self.Attmheight == 1:
                self.sendToSpike("Attachment.run_for_rotations(-2)")
            
    

class App:
    async def exec(self, spike: Spike):
        self.window = Window(asyncio.get_event_loop(), spike)
        await self.window.Freewindow()


class Window(tk.Tk):
    def __init__(self, loop, spike: Spike):
        self.spike = spike
        self.run = True
        self.loop = loop
        self.root = tk.Tk()
        #window setup
        self.root.title('FreeMode')
        self.root.geometry("1500x900+10+10")
        self.root.configure(bg='lightgray')
        self.createCanvas()
        self.quit = tk.Button(self.root, text="quit", fg='blue', font=("Helvetica", 40), command=self.stop)
        self.quit.place(x=1269,y=700)
        self.createLabels()
        self.setupCmds()
        self.root.update()

    def stop(self):
        self.run = False

    def createLabels(self):
        #
        self.speed = tk.Label(self.root, text="Geschwindigkeit:", fg='blue', font=("Helvetica", 30))
        self.speed.place(x=900, y=150)
        self.speed2=tk.Label(self.root, text= "Test", fg='blue', font=("Helvetica", 30))
        self.speed2.place(x=1300, y=150)
        #
        self.distance=tk.Label(self.root, text="Abstand:", fg='blue', font=("Helvetica", 30))
        self.distance.place(x=900, y=200)
        self.distance2=tk.Label(self.root, text="Test", fg='blue', font=("Helvetica", 30))
        self.distance2.place(x=1300, y=200)
        #
        self.steering=tk.Label(self.root, text="Winkel Steuerung:", fg='blue', font=("Helvetica", 30))
        self.steering.place(x=900, y=250)
        self.steering2=tk.Label(self.root, text="Test", fg='blue', font=("Helvetica", 30))
        self.steering2.place(x=1300, y=250)
        #
        self.attachment=tk.Label(self.root, text="Position Gerät:", fg='blue', font=("Helvetica", 30))
        self.attachment.place(x=900, y=300)
        self.attachment2=tk.Label(self.root, text="Test", fg='blue', font=("Helvetica", 30))
        self.attachment2.place(x=1300, y=300)
        #
        self.chassis=tk.Label(self.root, text="Position Chassis:", fg='blue', font=("Helvetica", 30))
        self.chassis.place(x=900, y=350)
        self.chassis2=tk.Label(self.root, text="Test", fg='blue', font=("Helvetica", 30))
        self.chassis2.place(x=1300, y=350)    

    def createCanvas(self):
        self.canvas = tk.Canvas(self.root, width = 1500, height = 900)
        self.canvas.grid()
   
    def setupCmds(self):
        keyboard.on_press_key("w", lambda _: self.spike.move(-100))
        keyboard.on_release_key("w",lambda _: self.spike.move(0))
        #backwards
        keyboard.on_press_key("s", lambda _: self.spike.move(75))
        keyboard.on_release_key("s",lambda _: self.spike.move(0))
        #left
        keyboard.on_press_key("a", lambda _: self.spike.steer(15))
        keyboard.on_release_key("a",lambda _: self.spike.steer(0))
        #right
        keyboard.on_press_key("d", lambda _: self.spike.steer(-15))
        keyboard.on_release_key("d",lambda _: self.spike.steer(0))
        #chassis up and down
        keyboard.on_press_key("y", lambda _:self.spike.Chassish(-1))
        keyboard.on_press_key("x",lambda _: self.spike.Chassish(1))
        #Attachment up and down
        keyboard.on_press_key("f", lambda _:self.spike.Attachmentheight(-1))
        keyboard.on_press_key("r", lambda _:self.spike.Attachmentheight(1))
    
    async def Freewindow(self):
        txt = 0
        while (self.run):
            # Wait some time
            await asyncio.sleep(.01)
            
            # Update the model
            self.spike.update()

            # Update the view
            # - update label texts
            if (self.spike.Abstand > -1):
                txt = str(self.spike.Abstand)
            else:
                txt = "fehler: zu große Entfernung"
            self.distance2.configure(text=txt)

            self.speed2.configure(text= str(self.spike.Test))
            self.steering2.configure(text= str(self.spike.Steeringangle))

            if self.spike.Chassisheight == -1:
                self.chassis2.configure(text= "lowered")
            else:
                self.chassis2.configure(text= "up")

            if self.spike.Attmheight == -1:
                self.attachment2.configure(text= "lowered")
            else:
                self.attachment2.configure(text= "up")

            # - update canvas
            self.canvas.delete("all")
            #left
            color = 'blue' if self.spike.SteeringAngle > 0 else 'black'
            self.canvas.create_polygon(100,500,200,600,200,400, outline = color, fill = color)
            self.canvas.create_rectangle( 200, 450, 350, 550, outline = color, fill = color)
            #forward
            color = 'blue' if self.spike.Speed < 0 else 'black'
            self.canvas.create_polygon( 425, 100, 325, 250, 525, 250, outline = color, fill = color)
            self.canvas.create_rectangle( 375, 250, 475, 400, outline = color, fill = color)
            #right
            color = 'blue' if self.spike.SteeringAngle < 0 else 'black'
            self.canvas.create_polygon( 750, 500, 650, 400, 650, 600, outline = color, fill = color)
            self.canvas.create_rectangle( 500, 450, 650, 550, outline = color, fill = color)
            #backwards
            color = 'blue' if self.spike.Speed > 0 else 'black'
            self.canvas.create_polygon( 425, 850, 325, 750, 525, 750, outline = color, fill = color)
            self.canvas.create_rectangle( 375, 600, 475, 750, outline = color, fill = color)
            
            self.root.update()


def Freerun():
    global Abstand
    global Abstandtxt
    global s
        
    #connencting with lego hub
    #first hub:  ac:1f:0f:1d:61:c1
    #second hub: 64:8c:bb:08:8f:24
    adapter_addr = "64:8c:bb:08:8f:24"
    port = 1  # Normal port for rfcomm?
    buf_size = 1024

    spike = Spike(adapter_addr, port)
    spike.connect()

    asyncio.run(App().exec(spike))
    
    spike.close()
    exit()
