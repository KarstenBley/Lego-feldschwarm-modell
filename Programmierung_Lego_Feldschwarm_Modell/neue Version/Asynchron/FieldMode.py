from curses import KEY_UP
from tkinter import Y
import keyboard
import math
import sys
from tkinter import *
import turtle

import time
import socket

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
      value = data[2:len(data)-2]
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
        valuesStr = data[2:len(data)-2]
        values = valuesStr.split(b',')
        return list(map(lambda x: int(x) if x != b'None' else -1, values))
    else:
        return list()
    

def sendwithtest(s: socket, cmd):
   data = sendToSpike(s, cmd)
   print(data)
   distancetest = getDistance(s)
   if (distancetest != -1):
      print(distancetest)
   while distancetest <= 5:
      print("blockiert")
      distancetest = getDistance(s)

def RunForRotations(s: socket, rota):
    global Abstand
    global rotations
    Abstand = 0
    speed = 0
    Steeringangle = 0
    rotations = 0
    r = 0
    data = sendToSpike(s, "AccelerationB.set_degrees_counted(0)")
    print(data)
    while True:
        if rota < 0:
            data = sendToSpike(s, "AccelerationB.start(-75)")
            print(data)
            r = -1
            rota = rota *-1
        elif rota > 0:
            data = sendToSpike(s, "AccelerationB.start(75)")
            print(data)
            r = 1            
        #
        values = getSensorData(s)
        if (len(values) == 4):
            Abstand = values[0]
            speed = values[1]
            Steeringangle = values[2]
            rotations = values[3]
            rotations = rotations / 360 * r
        distancetest = Abstand
        #
        if (distancetest != -1):
            print(distancetest)
        while distancetest <= 5 and distancetest >= 0:
            print("blockiert")
            data = sendToSpike(s, "AccelerationB.stop()")
            print(data)
            distancetest = getDistance(s)
        #
        if rotations >= rota:
            data = sendToSpike(s, "AccelerationB.stop()")
            print(data)
            break

   




def runfieldmode(y,b,anz):
   #print(y,b)
   
   a = 0
   x = 0
   bnz = 0
   
   #connecting with lego hub
   #first hub:  ac:1f:0f:1d:61:c1
   #second hub: 64:8c:bb:08:8f:24
   adapter_addr = "64:8c:bb:08:8f:24"
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
   data =sendToSpike(s, "from spike import Motor, DistanceSensor")
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

   while a < b:
      
        #lower chassis and attachment
        sendToSpike(s, "Chassis.run_for_rotations(5)")
        print(data)

        sendToSpike(s, "Attachment.run_for_rotations(2)")
        print(data)
        
        #Field = Tk()
        #Status = Label(Field,text = "Status:", fg='blue', font=("Helvetica", 40))
        #Status.place(x = 400,y = 500)
        #Statusanzeige = Label(Field, text = "Feldbearbeitung laufend", fg='blue', font=("Helvetica", 40))
        #Statusanzeige.place(x = 600, y = 500)
      
        #print(x,y)
        RunForRotations(s,y*3)
        if (a % 2) == 0:
            
            #turn right
            sendToSpike(s, "Attachment.run_for_rotations(-2)")
            print(data)
            #
            sendToSpike(s, "SteeringE.run_for_degrees(-35)")
            print(data)
            #
            f = 0
            RunForRotations(s,-19)
            #
            #turtle.circle(-50,90)
            #turtle.forward(30)
            #
            sendToSpike(s, "SteeringE.run_for_degrees(35)")
            print(data)
            #
            while bnz < anz:
                RunForRotations(s,-3)
                
                
                print(data)
                bnz = bnz +1
            #
            bnz = 0
            #
            sendToSpike(s, "SteeringE.run_for_degrees(35)")
            print(data)
            #
            f = 0
            RunForRotations(s,19)
            #
            #turtle.circle(50,-90)
            #
            sendToSpike(s, "SteeringE.run_for_degrees(-35)")
            print(data)
            #
            f = 0
            RunForRotations(s,-15)
            #
            #turtle.forward(100)
            #
            sendToSpike(s, "Attachment.run_for_rotations(2)")
            print(data)
            
            a = a + 1
            x = 0
            #print(a,b)
            print("wenden1")
        else :
            
            #turn left
            sendToSpike(s, "Attachment.run_for_rotations(-2)")
            print(data)
            #
            sendToSpike(s, "SteeringE.run_for_degrees(35)")
            print(data)
            #
            f = 0
            RunForRotations(s,-19)
            #
            sendToSpike(s, "SteeringE.run_for_degrees(-35)")
            print(data)
            #
            while bnz < anz:
                RunForRotations(s,-3)
                print(data)
                bnz = bnz +1
            #
            bnz = 0
            #
            sendToSpike(s, "SteeringE.run_for_degrees(-35)")
            print(data)
            #
            f = 0
            RunForRotations(s,19)
            #
            sendToSpike(s, "SteeringE.run_for_degrees(35)")
            print(data)
            #
            f = 0
            RunForRotations(s,-15)
            #
            sendToSpike(s, "Attachment.run_for_rotations(2)")
            print(data)
            
            a = a + 1
            x = 0
            #print(a,b)
            print("wenden2")
               
         #quit=Button(Field, text="quit", fg='blue', font=("Helvetica", 40), command=lambda:[stop(), Field.destroy()])
         #quit.place(x=1269,y=700)
         
         #Field.geometry("1500x900+10+10")
         #Field.title('FieldMode')
         #Field.configure(bg = 'lightgray')
         #Field.mainloop()
         
        
        #Statusanzeige.configure(text="fertig")
      
        #raise attachment and chassis   
        sendToSpike(s, "Chassis.run_for_rotations(-5)")
        print(data)

        sendToSpike(s, "Attachment.run_for_rotations(-2)")
        print(data) 

        #loop break
        """
        if running == False:
           break
        """
        """
        if Field.destroy:
           break       
        """
        text = input()
        if text == "quit":
           break
         
        break
   exit()
