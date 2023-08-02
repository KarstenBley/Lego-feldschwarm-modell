from curses import KEY_UP
from typing import Text
import keyboard
import threading
import math
import sys
from tkinter import *
import turtle

import time
import socket

PositionA = int
speedB = int
PositionC = int
angleE = int
distanceD = float
running = bool
running = True

def stop():
    global running
    running = False


def sendToSpike(s: socket, cmd: str):
    eot = b'\x04' + b'\x04' + bytes('>', 'UTF-8')

    # sendToSpike the command
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
    global valuedistance2
    dataDistance = sendToSpike(s, "print(DistanceSensorD.get_distance_cm())")
    if (dataDistance.startswith(bytes('OK', 'UTF-8')) and dataDistance.endswith(bytes('\r\n', 'UTF-8'))):
        valuedistance2 = dataDistance[2:len(dataDistance)-2]
        print(valuedistance2)
        if valuedistance2 != b'None' and not valuedistance2.startswith(bytes('OK', 'UTF-8')):
            valuedistance = int(valuedistance2)
        else:
            valuedistance = -1
        return valuedistance
    else:
        return -2
    
def getSpeed(s: socket):
    global valuespeed2
    dataSpeed = sendToSpike(s, "print(AccelerationB.get_speed())")
    if (dataSpeed.startswith(bytes('OK', 'UTF-8')) and dataSpeed.endswith(bytes('\r\n', 'UTF-8'))):
        valuespeed2 = dataSpeed[2:len(dataSpeed)-2]
        if valuespeed2 != b'None':
            valuespeed = int(valuespeed2)
        else:
            valuespeed = -1
            
        return valuespeed


def Freerun():
    global distance
    global speed
    global Geschw
    global Abstand
    global Abstandtxt
    global canvas
    global Freew

    Freew = Tk()
    Freew.title('FreeMode')
    Freew.geometry("1500x900+10+10")
    Freew.configure(bg='lightgray')
    Freew.update()
    while True:
        
        #connencting with lego hub
        adapter_addr = "64:8C:BB:08:8F:24"
        port = 1  # Normal port for rfcomm?
        buf_size = 1024

        global s 
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
        
        print(data)

        #setting up hub
        sendToSpike(s,"from spike import Motor, DistanceSensor")
        print(data)

        sendToSpike(s,"AccelerationB = Motor('B')")
        print(data)

        sendToSpike(s,"DistanceSensorD = DistanceSensor('D')")
        
        print(data)

        sendToSpike(s,"SteeringE = Motor('E')")
        
        print(data)

        sendToSpike(s,"Chassis = Motor('C')")
        
        print(data)

        sendToSpike(s,"Attachment = Motor('A')")
        
        print(data)

        sendToSpike(s,"SteeringE.set_stall_detection(True)")
        
        print(data)

        sendToSpike(s,"Chassis.set_stall_detection(True)")
        
        print(data)

        sendToSpike(s,"SteeringE.set_degrees_counted(0)")
        
        print(data)

        sendToSpike(s,"Chassis.set_degrees_counted(0)")
        
        print(data)

        sendToSpike(s,"Attachment.set_degrees_counted(0)")
        
        print(data)

        sendToSpike(s,"AccelerationB.set_degrees_counted(0)")
        
        print(data)                  

        sendToSpike(s,"SteeringE.set_stop_action('hold')")
        
        print(data)

        sendToSpike(s,"hub.display.show('hello')")
        
        print(data)

        sendToSpike(s,"DistanceSensorD.light_up_all(100)")
        
        print(data)

        x = 0

        canvas = Canvas(Freew, width = 1500, height = 900)
        #forward
        canvas.create_polygon(100,500,200,600,200,400, outline = 'black', fill = 'black')
        canvas.create_rectangle( 200, 450, 350, 550, outline = 'black', fill = 'black')
        #left
        canvas.create_polygon( 425, 100, 325, 250, 525, 250, outline = 'black', fill = 'black')
        canvas.create_rectangle( 375, 250, 475, 400, outline = 'black', fill = 'black')
        #right
        canvas.create_polygon( 750, 500, 650, 400, 650, 600, outline = 'black', fill = 'black')
        canvas.create_rectangle( 500, 450, 650, 550, outline = 'black', fill = 'black')
        #backwards
        canvas.create_polygon( 425, 850, 325, 750, 525, 750, outline = 'black', fill = 'black')
        canvas.create_rectangle( 375, 600, 475, 750, outline = 'black', fill = 'black')
        canvas.grid()
    
        #
        speed=Label(Freew, text="Geschwindigkeit:", fg='blue', font=("Helvetica", 30))
        speed.place(x=900, y=150)
        speed=Label(Freew, text= "Test", fg='blue', font=("Helvetica", 30))
        speed.place(x=1300, y=150)
        #
        distance=Label(Freew, text="Abstand:", fg='blue', font=("Helvetica", 30))
        distance.place(x=900, y=200)
        distance=Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
        distance.place(x=1300, y=200)
        #
        steering=Label(Freew, text="Winkel Steuerung:", fg='blue', font=("Helvetica", 30))
        steering.place(x=900, y=250)
        steering=Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
        steering.place(x=1300, y=250)
        #
        attachment=Label(Freew, text="Position Gerät:", fg='blue', font=("Helvetica", 30))
        attachment.place(x=900, y=300)
        attachement=Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
        attachement.place(x=1300, y=300)
        #
        chassis=Label(Freew, text="Position Chassis:", fg='blue', font=("Helvetica", 30))
        chassis.place(x=900, y=350)
        chassis=Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
        chassis.place(x=1300, y=350)

        quit = Button(Freew, text="quit", fg='blue', font=("Helvetica", 40), command=lambda:[stop(), Freew.destroy(), s.close()])
        quit.place(x=1269,y=700)
        
        keyboard.on_press_key("w", lambda _:sendToSpike(s,"AccelerationB.start(-100)"))
        keyboard.on_press_key("w", lambda _:canvas.create_polygon(425, 100, 325, 250, 525, 250, outline = 'blue', fill = 'blue'))
        keyboard.on_press_key("w", lambda _:canvas.create_rectangle( 375, 250, 475, 400, outline = 'blue', fill = 'blue'))
        keyboard.on_release_key("w",lambda _: sendToSpike(s,"AccelerationB.stop()"))
        keyboard.on_release_key("w", lambda _:canvas.create_polygon(425, 100, 325, 250, 525, 250, outline = 'black', fill = 'black'))
        keyboard.on_release_key("w", lambda _:canvas.create_rectangle( 375, 250, 475, 400, outline = 'black', fill = 'black'))
        #backwards
        keyboard.on_press_key("s", lambda _:sendToSpike(s,"AccelerationB.start(75)"))
        keyboard.on_press_key("s", lambda _:canvas.create_polygon(425, 850, 325, 750, 525, 750, outline = 'blue', fill = 'blue'))
        keyboard.on_press_key("s", lambda _:canvas.create_rectangle( 375, 600, 475, 750, outline = 'blue', fill = 'blue'))
        keyboard.on_release_key("s",lambda _: sendToSpike(s,"AccelerationB.stop()"))
        keyboard.on_release_key("s", lambda _:canvas.create_polygon(425, 850, 325, 750, 525, 750, outline = 'black', fill = 'black'))
        keyboard.on_release_key("s", lambda _:canvas.create_rectangle( 375, 600, 475, 750, outline = 'black', fill = 'black'))
        #left
        keyboard.on_press_key("a", lambda _:sendToSpike(s,"SteeringE.start(15)"))
        keyboard.on_press_key("a", lambda _:canvas.create_polygon(100,500,200,600,200,400, outline = 'blue', fill = 'blue'))
        keyboard.on_press_key("a", lambda _:canvas.create_rectangle( 200, 450, 350, 550, outline = 'blue', fill = 'blue'))
        keyboard.on_release_key("a",lambda _: sendToSpike(s,"SteeringE.stop()"))
        keyboard.on_release_key("a", lambda _:canvas.create_polygon(100,500,200,600,200,400, outline = 'black', fill = 'black'))
        keyboard.on_release_key("a", lambda _:canvas.create_rectangle( 200, 450, 350, 550, outline = 'black', fill = 'black'))
        #right
        keyboard.on_press_key("d", lambda _:sendToSpike(s,"SteeringE.start(-15)"))
        keyboard.on_press_key("d", lambda _:canvas.create_polygon(750, 500, 650, 400, 650, 600, outline = 'blue', fill = 'blue'))
        keyboard.on_press_key("d", lambda _:canvas.create_rectangle( 500, 450, 650, 550, outline = 'blue', fill = 'blue'))
        keyboard.on_release_key("d",lambda _: sendToSpike(s,"SteeringE.stop()"))
        keyboard.on_release_key("d", lambda _:canvas.create_polygon(750, 500, 650, 400, 650, 600, outline = 'black', fill = 'black'))
        keyboard.on_release_key("d", lambda _:canvas.create_rectangle( 500, 450, 650, 550, outline = 'black', fill = 'black'))
        #chassis up and down
        keyboard.on_press_key("y", lambda _:sendToSpike(s,"Chassis.run_for_rotations(5)"))
        keyboard.on_press_key("x",lambda _: sendToSpike(s,"Chassis.run_for_rotations(-5)"))
        #Attachment up and down
        keyboard.on_press_key("f", lambda _:sendToSpike(s,"Attachment.run_for_rotations(2)"))
        keyboard.on_press_key("r", lambda _:sendToSpike(s,"Attachment.run_for_rotations(-2)"))
        keyboard.on_press_key("u", lambda _:stop)

        x = threading.Thread(target=updatecanvas)
        x.start()
        Freew.mainloop()
        
        sendToSpike(s,"hub.display.show()")
        
        print(data)

        sendToSpike(s,"DistancesensorD.light_up_all(0)")
        
        print(data)
        sendToSpike(s,"DistancesensorD.light_up_all(100)")
        
        print(data)
        sendToSpike(s,"DistancesensorD.light_up_all(0)")
        
        print(data)    
        s.close()
        exit()

def updatecanvas():
    while True:
        Accelerated = True
        
        Abstand = getDistance(s)
        if (Abstand > -1):
            Abstandtxt = str(Abstand)
        else:
            Abstandtxt = "fehler: zu große Entfernung"

        Geschw = getSpeed(s)
        if (Geschw or Geschw == 0):
            
            Geschw = Geschw * -1
            if (Geschw > -1):
                Geschwtxt = str(Geschw)
            else:
                Geschwtxt = "fehler beim lesen der geschwindgkeit"
            speed.config(text= Geschwtxt)
        distance.config(text= Abstandtxt)
        time.sleep(0.2)
        