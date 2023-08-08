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
         print("systemFehler, überprüfen sie die Rechtschreibung der Befehle")
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
    

def sendwithtest(s: socket, cmd):
   data = sendToSpike(s, cmd)
   print(data)
   distancetest = getDistance(s)
   if (distancetest != -1):
      print(distancetest)
   while distancetest <= 5:
      print("blockiert")
      distancetest = getDistance(s)



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

   #connecting second lego hub
   if bnz == 2:
      adapter_addr2 = ""
      port2 = 1  # Normal port for rfcomm?
      buf_size = 1024

      s2 = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
      s2.connect((adapter_addr2, port2))

      time.sleep(0.1)
      data = s.recv(1024)
      print(data)

      s2.send(b'\x03')
      time.sleep(0.1)
      s2.send(b'\x01')
      data = s.recv(1024)
      print(data)

      #setting up second hub
      data = sendToSpike(s2,"from spike import Motor, DistanceSensor")
      print(data)

      data = sendToSpike(s2,"AccelerationB = Motor('B')")
      print(data)

      data = sendToSpike(s2,"SteeringE = Motor('E')")
      print(data)

      data = sendToSpike(s2,"Chassis = Motor('C')")
      print(data)

      data = sendToSpike(s2,"Attachment = Motor('A')")
      print(data)

      data = sendToSpike(s2,"DistanceSensorD = DistanceSensor('D')")
      print(data)

      data = sendToSpike(s2,"SteeringE.set_stall_detection(True)")
      print(data)

      data = sendToSpike(s2,"SteeringE.set_stop_action('hold')")
      print(data)

      data = sendToSpike(s2,"hub.display.show('hello')")
      print(data)

      data = sendToSpike(s2,"DistanceSensorD.light_up_all(100)")
      print(data)
   
   #turtle.goto()

   #turtle.penup()
   #turtle.goto(-400,350)
   #turtle.speed(1)
   
   while a < b:
      
      #lower chassis and attachment
      sendwithtest(s, "Chassis.run_for_rotations(5)")
      print(data)

      sendwithtest(s, "Attachment.run_for_rotations(2)")
      print(data)
      
      #Field = Tk()
      #Status = Label(Field,text = "Status:", fg='blue', font=("Helvetica", 40))
      #Status.place(x = 400,y = 500)
      #Statusanzeige = Label(Field, text = "Feldbearbeitung laufend", fg='blue', font=("Helvetica", 40))
      #Statusanzeige.place(x = 600, y = 500)
      
      #print(x,y)
      while a < b:
         
         #drive forward
         sendwithtest(s, "AccelerationB.run_for_rotations(-3)")
         print(data)
         x = x + 1
         #turtle.forward(10)
         
         print("geradeaus")
         if x == y:
            if (a % 2) == 0:
               
               #turn right
               sendwithtest(s, "Attachment.run_for_rotations(-2)")
               print(data)
               #
               sendwithtest(s, "SteeringE.run_for_degrees(-35)")
               print(data)
               #
               f = 0
               while f < 19:
                  sendwithtest(s, "AccelerationB.run_for_rotations(-1)")
                  print(data)
                  f = f+1
               #
               #turtle.circle(-50,90)
               #turtle.forward(30)
               #
               sendwithtest(s, "SteeringE.run_for_degrees(35)")
               print(data)
               #
               while bnz < anz:
                  sendwithtest(s, "AccelerationB.run_for_rotations(-3)")
                  
                  
                  print(data)
                  bnz = bnz +1
               #
               bnz = 0
               #
               sendwithtest(s, "SteeringE.run_for_degrees(35)")
               print(data)
               #
               f = 0
               while f < 19:
                  sendwithtest(s, "AccelerationB.run_for_rotations(1)")
                  print(data)
                  f = f+1
               #
               #turtle.circle(50,-90)
               #
               sendwithtest(s, "SteeringE.run_for_degrees(-35)")
               print(data)
               #
               f = 0
               while f < 15:
                  sendwithtest(s, "AccelerationB.run_for_rotations(-1)")
                  print(data)
                  f = f+1
               #
               #turtle.forward(100)
               #
               sendwithtest(s, "Attachment.run_for_rotations(2)")
               print(data)
               
               a = a + 1
               x = 0
               #print(a,b)
               print("wenden1")
            else :
               
               #turn left
               sendwithtest(s, "Attachment.run_for_rotations(-2)")
               print(data)
               #
               sendwithtest(s, "SteeringE.run_for_degrees(35)")
               print(data)
               #
               f = 0
               while f < 15:
                  sendwithtest(s, "AccelerationB.run_for_rotations(-1)")
                  print(data)
                  f = f+1
               #
               sendwithtest(s, "SteeringE.run_for_degrees(-35)")
               print(data)
               #
               while bnz < anz:
                  sendwithtest(s, "AccelerationB.run_for_rotations(-3)")
                  print(data)
                  bnz = bnz +1
               #
               bnz = 0
               #
               sendwithtest(s, "SteeringE.run_for_degrees(-35)")
               print(data)
               #
               f = 0
               while f < 19:
                  sendwithtest(s, "AccelerationB.run_for_rotations(19)")
                  print(data)
                  f = f+1
               #
               sendwithtest(s, "SteeringE.run_for_degrees(35)")
               print(data)
               #
               f = 0
               while f < 15:
                  sendwithtest(s, "AccelerationB.run_for_rotations(-15)")
                  print(data)
                  f = f+1
               #
               sendwithtest(s, "Attachment.run_for_rotations(2)")
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
      sendwithtest(s, "Chassis.run_for_rotations(-5)")
      print(data)

      sendwithtest(s, "Attachment.run_for_rotations(-2)")
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

   #blink   
   sendwithtest(s, "DistancesensorD.light_up_all(0)")
   print(data)
   sendwithtest(s, "DistancesensorD.light_up_all(100)")
   print(data)
   sendwithtest(s, "DistancesensorD.light_up_all(0)")
   print(data)
   s.close()
   exit()
