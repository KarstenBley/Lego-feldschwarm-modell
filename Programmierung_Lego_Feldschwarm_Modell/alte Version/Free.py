from curses import KEY_UP
from typing import Text
import keyboard
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

def Freerun():
    while True:
        
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
        s.send(bytes("from spike import Motor, DistanceSensor, hub", 'UTF-8') + b'\x04')
        data = s.recv(1024)
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

        x = 0
        while  1:
            
            #free mode window
            Freew=Tk()
            
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
            speed2=Label(Freew, text= "Test", fg='blue', font=("Helvetica", 30))
            speed2.place(x=1300, y=150)
            #
            distance=Label(Freew, text="Abstand:", fg='blue', font=("Helvetica", 30))
            distance.place(x=900, y=200)
            distance=Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
            distance.place(x=1300, y=200)
            #
            steering=Label(Freew, text="Winkel Steuerung:", fg='blue', font=("Helvetica", 30))
            steering.place(x=900, y=250)
            distance=Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
            distance.place(x=1300, y=250)
            #
            attachment=Label(Freew, text="Position Gerät:", fg='blue', font=("Helvetica", 30))
            attachment.place(x=900, y=300)
            distance=Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
            distance.place(x=1300, y=300)
            #
            chassis=Label(Freew, text="Position Chassis:", fg='blue', font=("Helvetica", 30))
            chassis.place(x=900, y=350)
            distance=Label(Freew, text="Test", fg='blue', font=("Helvetica", 30))
            distance.place(x=1300, y=350)
            """
            global PositionA
            global speedB
            global PositionC
            global angleE
            global distanceD
            """
            #forward
            keyboard.on_press_key("w", lambda _:s.send(bytes("AccelerationB.start(-100)", 'UTF-8') + b'\x04'))
            keyboard.on_press_key("w", lambda _:canvas.create_polygon(425, 100, 325, 250, 525, 250, outline = 'blue', fill = 'blue'))
            keyboard.on_press_key("w", lambda _:canvas.create_rectangle( 375, 250, 475, 400, outline = 'blue', fill = 'blue'))
            keyboard.on_release_key("w",lambda _: s.send(bytes("AccelerationB.stop()", 'UTF-8') + b'\x04'))
            keyboard.on_release_key("w", lambda _:canvas.create_polygon(425, 100, 325, 250, 525, 250, outline = 'black', fill = 'black'))
            keyboard.on_release_key("w", lambda _:canvas.create_rectangle( 375, 250, 475, 400, outline = 'black', fill = 'black'))
            #backwards
            keyboard.on_press_key("s", lambda _:s.send(bytes("AccelerationB.start(75)", 'UTF-8') + b'\x04'))
            keyboard.on_press_key("s", lambda _:canvas.create_polygon(425, 850, 325, 750, 525, 750, outline = 'blue', fill = 'blue'))
            keyboard.on_press_key("s", lambda _:canvas.create_rectangle( 375, 600, 475, 750, outline = 'blue', fill = 'blue'))
            keyboard.on_release_key("s",lambda _: s.send(bytes("AccelerationB.stop()", 'UTF-8') + b'\x04'))
            keyboard.on_release_key("s", lambda _:canvas.create_polygon(425, 850, 325, 750, 525, 750, outline = 'black', fill = 'black'))
            keyboard.on_release_key("s", lambda _:canvas.create_rectangle( 375, 600, 475, 750, outline = 'black', fill = 'black'))
            #left
            keyboard.on_press_key("a", lambda _:s.send(bytes("SteeringE.start(15)", 'UTF-8') + b'\x04'))
            keyboard.on_press_key("a", lambda _:canvas.create_polygon(100,500,200,600,200,400, outline = 'blue', fill = 'blue'))
            keyboard.on_press_key("a", lambda _:canvas.create_rectangle( 200, 450, 350, 550, outline = 'blue', fill = 'blue'))
            keyboard.on_release_key("a",lambda _: s.send(bytes("SteeringE.stop()", 'UTF-8') + b'\x04'))
            keyboard.on_release_key("a", lambda _:canvas.create_polygon(100,500,200,600,200,400, outline = 'black', fill = 'black'))
            keyboard.on_release_key("a", lambda _:canvas.create_rectangle( 200, 450, 350, 550, outline = 'black', fill = 'black'))
            #right
            keyboard.on_press_key("d", lambda _:s.send(bytes("SteeringE.start(-15)", 'UTF-8') + b'\x04'))
            keyboard.on_press_key("d", lambda _:canvas.create_polygon(750, 500, 650, 400, 650, 600, outline = 'blue', fill = 'blue'))
            keyboard.on_press_key("d", lambda _:canvas.create_rectangle( 500, 450, 650, 550, outline = 'blue', fill = 'blue'))
            keyboard.on_release_key("d",lambda _: s.send(bytes("SteeringE.stop()", 'UTF-8') + b'\x04'))
            keyboard.on_release_key("d", lambda _:canvas.create_polygon(750, 500, 650, 400, 650, 600, outline = 'black', fill = 'black'))
            keyboard.on_release_key("d", lambda _:canvas.create_rectangle( 500, 450, 650, 550, outline = 'black', fill = 'black'))
            #chassis up and down
            keyboard.on_press_key("y", lambda _:s.send(bytes("Chassis.run_for_rotations(5)", 'UTF-8') + b'\x04'))
            keyboard.on_press_key("x",lambda _: s.send(bytes("Chassis.run_for_rotations(-5)", 'UTF-8') + b'\x04'))
            #Attachment up and down
            keyboard.on_press_key("f", lambda _:s.send(bytes("Attachment.run_for_rotations(2)", 'UTF-8') + b'\x04'))
            keyboard.on_press_key("r", lambda _:s.send(bytes("Attachment.run_for_rotations(-2)", 'UTF-8') + b'\x04'))
            keyboard.on_press_key("u", lambda _:stop)

            #quit button
            quit=Button(Freew, text="quit", fg='blue', font=("Helvetica", 40), command=lambda:[stop(), Freew.destroy()])
            quit.place(x=1269,y=700)
        
            #window setup
            Freew.title('FreeMode')
            Freew.geometry("1500x900+10+10")
            Freew.configure(bg='lightgray')
            Freew.mainloop()

            #loop break
            if Freew.destroy:
                break
            
            
            """#
            s.send(bytes("PositionA = Attachment.get_degrees_counted()", 'UTF-8') + b'\x04')
            s.send(bytes("speedB = AccelerationA.get_speed()", 'UTF-8') + b'\x04')
            s.send(bytes("PositionC = Chassis.get_degrees_counted()", 'UTF-8') + b'\x04')
            s.send(bytes("angleE = steering.get_degrees_counted()", 'UTF-8') + b'\x04')
            s.send(bytes("distanceD = DistancesensorD.get_distance_cm()", 'UTF-8') + b'\x04')
    	    """
            #print(PositionA,speedB,PositionC,angleE,distanceD)
            if running == False:
                break

            text = input()
            
            #loop break
            if text == "quit":
                break
        
        s.send(bytes("hub.display.show()", 'UTF-8') + b'\x04')
        data = s.recv(1024)
        print(data)

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
