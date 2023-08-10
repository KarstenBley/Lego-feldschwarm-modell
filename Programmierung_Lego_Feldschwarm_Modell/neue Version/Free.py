from curses import KEY_UP
from typing import Text
import keyboard
import threading
import math
import sys
import tkinter as Tk
from PIL import Image, ImageTk
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
coordinatesX = [425]
coordinatesY = [500]
obstaclesX = []
obstaclesY = []
offsetX = 0
offsetY = 0
isRunning = False

def stop():
    global running
    running = False


def sendToSpike(s: socket, cmd: str):
    isRunning = True
    eot = b'\x04' + b'\x04' + bytes('>', 'UTF-8')
    neot = b'\r\n' + b'\x04' + bytes('>', 'UTF-8')

    # sendToSpike the command
    s.send(bytes(cmd, 'UTF-8') + b'\x04')
    data = bytearray()

    # Read until EOT is received
    while 1:
        tmp = s.recv(1024)
        data.extend(tmp)
        if (data.endswith(eot)):
            break
        if (data.endswith(neot)):
            print("fatal error (lol)")
            break
    return bytes(data[:len(data) - 3])

def getDistance(s: socket):
    global valuedistance2
    dataDistance = sendToSpike(s, "print(DistanceSensorD.get_distance_cm())")
    if (dataDistance.startswith(bytes('OK', 'UTF-8')) and dataDistance.endswith(bytes('\r\n', 'UTF-8'))):
        valuedistance2 = dataDistance[2:len(dataDistance)-2]
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
        if valuespeed2 != b'None' and not valuespeed2.startswith(bytes('OK', 'UTF-8')):
            valuespeed = int(valuespeed2)
        else:
            valuespeed = "Error"
        return valuespeed

def getAngle(s: socket):
    global valueAngle2
    dataAngle = sendToSpike(s, "print(SteeringE.get_degrees_counted())")
    if (dataAngle.startswith(bytes('OK', 'UTF-8')) and dataAngle.endswith(bytes('\r\n', 'UTF-8'))):
        valueAngle2 = dataAngle[2:len(dataAngle)-2]
        if valueAngle2 != b'None' and not valueAngle2.startswith(bytes('OK', 'UTF-8')):
            valueAngle = int(valueAngle2)
        else:
            valueAngle = "Error"
            
        return valueAngle
    
def isStalled(s: socket):
    global valueStalled2
    dataStalled = sendToSpike(s, "print(SteeringE.was_stalled())")
    if (dataStalled.startswith(bytes('OK', 'UTF-8')) and dataStalled.endswith(bytes('\r\n', 'UTF-8'))):
        valueStalled2 = dataStalled[2:len(dataStalled)-2]
        if valueStalled2.startswith(bytes('True', 'UTF-8')):
            return True
    return False


def Freerun():
    global distance
    global speed
    global steering
    global Geschw
    global Abstand
    global Abstandtxt
    global canvas
    global Freew

    Freew = Tk.Tk()
    Freew.title('FreeMode')
    Freew.geometry("1500x900+10+10")
    Freew.configure(bg='lightgray')
    Freew.update()
    while True:
        
        #connencting with lego hub
        adapter_addr = "ac:1f:0f:1d:61:c1"
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

        canvas = Tk.Canvas(Freew, width = 1500, height = 900)
        canvas.grid()
        
        canvas.create_rectangle( 50, 50, 800, 800, outline = 'gray', fill = 'gray')
        #
        speed=Tk.Label(Freew, text="Geschwindigkeit:", fg='blue', font=("Helvetica", 30))
        speed.place(x=900, y=150)
        speed=Tk.Label(Freew, text= "Test", fg='blue', font=("Helvetica", 30))
        speed.place(x=1300, y=150)
        #
        distance=Tk.Label(Freew, text="Abstand:", fg='blue', font=("Helvetica", 30))
        distance.place(x=900, y=200)
        distance=Tk.Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
        distance.place(x=1300, y=200)
        #
        steering=Tk.Label(Freew, text="Winkel Steuerung:", fg='blue', font=("Helvetica", 30))
        steering.place(x=900, y=250)
        steering=Tk.Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
        steering.place(x=1300, y=250)
        #
        attachment=Tk.Label(Freew, text="Position Gerät:", fg='blue', font=("Helvetica", 30))
        attachment.place(x=900, y=300)
        attachement=Tk.Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
        attachement.place(x=1300, y=300)
        #
        chassis=Tk.Label(Freew, text="Position Chassis:", fg='blue', font=("Helvetica", 30))
        chassis.place(x=900, y=350)
        chassis=Tk.Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
        chassis.place(x=1300, y=350)

        quit = Tk.Button(Freew, text="quit", fg='blue', font=("Helvetica", 40), command=lambda:[stop(), Freew.destroy(), s.close()])
        quit.place(x=1269,y=700)
        
        x = threading.Thread(target=updatecanvas)
        x.start()
                
        keyboard.on_press_key("w", lambda _:sendToSpike(s,"AccelerationB.start(-100)"))
        keyboard.on_release_key("w",lambda _: sendToSpike(s,"AccelerationB.stop()"))
        #backwards
        keyboard.on_press_key("s", lambda _:sendToSpike(s,"AccelerationB.start(75)"))
        keyboard.on_release_key("s",lambda _: sendToSpike(s,"AccelerationB.stop()"))
        #left
        keyboard.on_press_key("a", lambda _:sendToSpike(s,"SteeringE.start(15)"))
        keyboard.on_release_key("a",lambda _: sendToSpike(s,"SteeringE.stop()"))
        #right
        keyboard.on_press_key("d", lambda _:sendToSpike(s,"SteeringE.start(-15)"))
        keyboard.on_release_key("d",lambda _: sendToSpike(s,"SteeringE.stop()"))
        #chassis up and down
        keyboard.on_press_key("y", lambda _:sendToSpike(s,"Chassis.run_for_rotations(5)"))
        keyboard.on_press_key("x", lambda _: sendToSpike(s,"Chassis.run_for_rotations(-5)"))
        #Attachment up and down
        keyboard.on_press_key("f", lambda _:sendToSpike(s,"Attachment.run_for_rotations(2)"))
        keyboard.on_press_key("r", lambda _:sendToSpike(s,"Attachment.run_for_rotations(-2)"))

        keyboard.on_press_key("u", lambda _:stop)

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
    IsMoving = False
    GeschwBuffer=0
    GeschwBufferMax = 50
    positionX = 425
    positionY = 500
    global coordinatesX
    global coordinatesY
    global obstaclesX
    global obstaclesY
    global offsetX
    global offsetY
    global arrow
    mapSize = 20
    obstacleX = 0
    obstacleY = 0
    rotation = 0
    Winkel2 = 0
    Geschw = 0
    Geschw2 = 0    
    gray = (128,128,128)
    image = Image.open(r"C:\Users\karst\Documents\GitHub\Lego-feldscwarm-modell\Programmierung_Lego_Feldschwarm_Modell\neue Version\Arrow.png")
    resized_img = image.resize((20, 20))
    
    img = ImageTk.PhotoImage(resized_img, master = canvas)
    arrow = Tk.Label(Freew, image=img, bd = 0)
    while not isStalled(s):
        distance.config(text = "Winkel wird eingestellt")
        steering.config(text = "Winkel wird eingestellt")
        speed.config(text= "Winkel wird eingestellt")
        sendToSpike(s, "SteeringE.run_for_degrees(100)")
    sendToSpike(s, "SteeringE.run_for_degrees(-45)")
    sendToSpike(s, "SteeringE.set_degrees_counted(0)")
    speed.config(text= "0")
    while True:
        Abstand = getDistance(s)
        Geschw = getSpeed(s)
        Winkel = getAngle(s)
        

        if (Abstand > -1):
            Abstand2 = Abstand
            Abstandtxt = str(Abstand)
        else:
            Abstand2 = 0
            Abstandtxt = "fehler: zu große Entfernung"
        if (Winkel or Winkel == 0):

            if (Winkel != "Error"):
                Winkel *=-1
                Winkeltxt = str(Winkel)
            else:
                Winkeltxt = "fehler beim lesen des Winkels"


        if (Geschw or Geschw == 0):
            
            Geschw = Geschw * -1
            if Geschw == "Error":
                Geschwtxt = "fehler beim lesen der geschwindgkeit"
                speed.config(text= Geschwtxt)

        if Geschw != None and Geschw != "":
            if Geschw != "Error":
                if GeschwBuffer > GeschwBufferMax and int(Geschw) >= 0:
                    Geschwtxt = str(Geschw)
                    Geschw2 = Geschw
                    speed.config(text= Geschwtxt)
                elif GeschwBuffer < -GeschwBufferMax and int(Geschw) <= 0:
                    Geschwtxt = str(Geschw)
                    Geschw2 = Geschw
                    speed.config(text= Geschwtxt)
                else:
                    GeschwBuffer += Geschw
                    
        if Winkel != None:
             if Winkel != "Error":
                 Winkeltxt = str(Winkel)
                 Winkel2 = Winkel
        rotation += Winkel2 * Geschw2 / 800
        if Geschw2 != 0:
            coordinatesX.append(positionX + Geschw2/mapSize * math.cos(math.radians(rotation))); 
            coordinatesY.append(positionY + Geschw2/mapSize * math.sin(math.radians(rotation)));

        if Abstand2 != 0:
            obstacleX = (positionX + offsetX+ (math.cos(math.radians(rotation)) * Abstand2 * 0.75)); 
            obstacleY = (positionY + offsetY+ (math.sin(math.radians(rotation)) * Abstand2 * 0.75));
            obstaclesX.append(obstacleX)
            obstaclesY.append(obstacleY)
            canvas.create_rectangle( obstacleX+5, obstacleY+5, obstacleX-5, obstacleY-5, outline = 'black', fill = 'black')
        if positionX + offsetX < 800 and positionY + offsetY < 800 and positionX + offsetX > 50 and positionY + offsetY > 50:
            i = canvas.create_line(positionX + offsetX, positionY + offsetY, coordinatesX[len(coordinatesX)-1] + offsetX, coordinatesY[len(coordinatesY)-1] + offsetY, fill = "red")
            arrow.place(x = positionX -10 + offsetX, y = positionY -10 + offsetY)
            rotated_img = resized_img.rotate(rotation*-1+180, resample=Image.BICUBIC, expand=False, fillcolor = gray)
            img = ImageTk.PhotoImage(rotated_img, master = canvas)
            arrow.config(image = img)
            arrow.image = img
        else:
            arrow.place(x = 10000, y = 10000)
            
        
        #resized_img = resized_img.rotate(Winkel2 * Geschw2 / 800)
        #img = ImageTk.PhotoImage(resized_img, master = canvas)
        if keyboard.is_pressed("+"):
            updateMap(1.2)
            mapSize /= 1.2
        if keyboard.is_pressed("-"):
            updateMap(0.8)
            mapSize /= 0.8

        if keyboard.is_pressed("up arrow"):
            offsetY -= 50
            updateMap(1)
        elif keyboard.is_pressed("down arrow"):
            offsetY += 50
            updateMap(1)
        elif keyboard.is_pressed("left arrow"):
            offsetX -= 50
            updateMap(1)
        elif keyboard.is_pressed("right arrow"):
            offsetX += 50
            updateMap(1)


        positionX = coordinatesX[len(coordinatesX)-1]
        positionY = coordinatesY[len(coordinatesY)-1]
        distance.config(text = Abstandtxt)
        steering.config(text = Winkeltxt)
        time.sleep(0.2)

def updateMap(zoomvalue):
    global coordinatesX
    global coordinatesY
    global obstaclesX
    global obstaclesY
    global offsetX
    global offsetY
    global arrow
    canvas.create_rectangle( 50, 50, 800, 800, outline = 'gray', fill = 'gray')
    for i in range(0, len(coordinatesX)):
        coordinatesX[i] *= zoomvalue
        coordinatesY[i] *= zoomvalue
        if i != 0:
            if coordinatesX[i] + offsetX < 800 and coordinatesY[i]  + offsetY < 800 and coordinatesX[i]  + offsetX > 50 and coordinatesY[i]  + offsetY > 50:
                print(coordinatesX[i])
                canvas.create_line(coordinatesX[i-1] + offsetX, coordinatesY[i-1] + offsetY, coordinatesX[i] + offsetX, coordinatesY[i] + offsetY, fill = "red")
    for i in range(0, len(obstaclesX)):
        obstaclesX[i] *= zoomvalue
        obstaclesY[i] *= zoomvalue
        if obstaclesX[i]  + offsetX < 800 and obstaclesY[i]  + offsetY < 800 and obstaclesX[i]  + offsetX > 50 and obstaclesY[i]  + offsetY > 50:
                canvas.create_rectangle(obstaclesX[i]+5 + offsetX, obstaclesY[i]+5 + offsetY, obstaclesX[i]-5 + offsetX, obstaclesY[i]-5+offsetY, fill = "black")