from curses import KEY_UP
from tkinter import Y
import keyboard
import math
import sys
from tkinter import *
import turtle
import GUI

import time
import socket

def test(y,b):
   print(y,b)

def stop():
   global running
   running = False


def runfieldmode(y,b,anz):
   #print(y,b)
   
   a = 0
   x = 0
   bnz = 0
   
   #connecting with lego hub
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
   s.send(bytes("import hub", 'UTF-8') + b'\x04')
   data = s.recv(1024)
   print(data)

   s.send(bytes("from spike import Motor, DistanceSensor", 'UTF-8') + b'\x04')
   data = s.recv(1024)
   print(data)

   s.send(bytes("AccelerationB = Motor('B')", 'UTF-8') + b'\x04')
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

   s.send(bytes("DistancesensorD = DistanceSensor('D')", 'UTF-8') + b'\x04')
   data = s.recv(1024)
   print(data)

   s.send(bytes("SteeringE.set_stall_detection(True)", 'UTF-8') + b'\x04')
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
      s2.send(bytes("import hub", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s2.send(bytes("from spike import Motor, DistanceSensor", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s2.send(bytes("AccelerationB = Motor('B')", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s2.send(bytes("SteeringE = Motor('E')", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s2.send(bytes("Chassis = Motor('C')", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s2.send(bytes("Attachment = Motor('A')", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s2.send(bytes("DistancesensorD = DistanceSensor('D')", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s2.send(bytes("SteeringE.set_stall_detection(True)", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s2.send(bytes("SteeringE.set_stop_action('hold')", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s2.send(bytes("hub.display.show('hello')", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s2.send(bytes("DistancesensorD.light_up_all(100)", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)
   
   #turtle.goto()

   #turtle.penup()
   #turtle.goto(-400,350)
   #turtle.speed(1)
   
   while a < b:
      
      #lower chassis and attachment
      s.send(bytes("Chassis.run_for_rotations(5)", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)

      s.send(bytes("Attachment.run_for_rotations(2)", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)
      """
      Field = Tk()
      Status = Label(Field,text = "Status:", fg='blue', font=("Helvetica", 40))
      Status.place(x = 400,y = 500)
      Statusanzeige = Label(Field, text = "Feldbearbeitung laufend", fg='blue', font=("Helvetica", 40))
      Statusanzeige.place(x = 600, y = 500)
      """
      #print(x,y)
      while a < b:
         
         #drive forward
         s.send(bytes("AccelerationB.run_for_rotations(-3)", 'UTF-8') + b'\x04')
         data = s.recv(1024)
         print(data)
         x = x + 1
         #turtle.forward(10)
         
         print("geradeaus")
         if x == y:
            if (a % 2) == 0:
               
               #turn right
               s.send(bytes("Attachment.run_for_rotations(-2)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("SteeringE.run_for_degrees(-35)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("AccelerationB.run_for_rotations(-19)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               #turtle.circle(-50,90)
               #turtle.forward(30)
               #
               s.send(bytes("SteeringE.run_for_degrees(35)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               while bnz < anz:
                  s.send(bytes("AccelerationB.run_for_rotations(-3)", 'UTF-8') + b'\x04')
                  data = s.recv(1024)
                  print(data)
                  bnz = bnz +1
               #
               bnz = 0
               #
               s.send(bytes("SteeringE.run_for_degrees(35)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("AccelerationB.run_for_rotations(19)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               #turtle.circle(50,-90)
               #
               s.send(bytes("SteeringE.run_for_degrees(-35)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("AccelerationB.run_for_rotations(-15)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               #turtle.forward(100)
               #
               s.send(bytes("Attachment.run_for_rotations(2)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               
               a = a + 1
               x = 0
               #print(a,b)
               print("wenden1")
            else :
               
               #turn left
               s.send(bytes("Attachment.run_for_rotations(-2)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("SteeringE.run_for_degrees(35)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("AccelerationB.run_for_rotations(-19)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("SteeringE.run_for_degrees(-35)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               while bnz < anz:
                  s.send(bytes("AccelerationB.run_for_rotations(-3)", 'UTF-8') + b'\x04')
                  data = s.recv(1024)
                  print(data)
                  bnz = bnz +1
               #
               bnz = 0
               #
               s.send(bytes("SteeringE.run_for_degrees(-35)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("AccelerationB.run_for_rotations(19)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("SteeringE.run_for_degrees(35)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("AccelerationB.run_for_rotations(-15)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               #
               s.send(bytes("Attachment.run_for_rotations(2)", 'UTF-8') + b'\x04')
               data = s.recv(1024)
               print(data)
               
               a = a + 1
               x = 0
               #print(a,b)
               print("wenden2")
         """      
         quit=Button(Field, text="quit", fg='blue', font=("Helvetica", 40), command=lambda:[stop(), Field.destroy()])
         quit.place(x=1269,y=700)
         
         Field.geometry("1500x900+10+10")
         Field.title('FieldMode')
         Field.configure(bg = 'lightgray')
         Field.mainloop()
         
        
      Statusanzeige.configure(text="fertig")
      """
      #raise attachment and chassis   
      s.send(bytes("Chassis.run_for_rotations(-5)", 'UTF-8') + b'\x04')
      data = s.recv(1024)
      print(data)
      s.send(bytes("Attachment.run_for_rotations(-2)", 'UTF-8') + b'\x04')
      data = s.recv(1024)
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
   s.send(bytes("DistancesensorD.light_up_all(0)", 'UTF-8') + b'\x04')
   data = s.recv(1024)
   print(data)
   s.send(bytes("DistancesensorD.light_up_all(100)", 'UTF-8') + b'\x04')
   data = s.recv(1024)
   print(data)
   s.send(bytes("DistancesensorD.light_up_all(0)", 'UTF-8') + b'\x04')
   data = s.recv(1024)
   print(data)
   s.close()
   exit()
