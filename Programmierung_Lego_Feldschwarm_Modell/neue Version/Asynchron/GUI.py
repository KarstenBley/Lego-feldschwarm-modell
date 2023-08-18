from cmath import pi
from doctest import master
from operator import truediv
from pydoc import text
import string
import tkinter as Tk
from turtle import window_width
import turtle
import Free
import FieldMode as FM
import threading
from webbrowser import get
import keyboard
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import Canvas
import time
import math


x = 0
Zustand = 0
rotations = 0
tracks = 0
fieldlength = int
fieldwidth = int
rotations = int
tracks = int
Anzahl = int
fl = 0
offsetX = 0
offsetY = 0
coordinatesX = [425]
coordinatesY = [500]
upDown = [False]
FM.mapSize = 20

def FreeMode():
    while TRUE:
        Free.Freerun()

def Fieldsetup():
    global canvas
    global Fieldwindow

    Fieldwindow=Tk.Tk()
    Fieldwindow.title('FieldMode')
    Fieldwindow.geometry("1500x900+10+10")
    Fieldwindow.configure(bg='lightgray')
    Fieldwindow.update()

    while True:
        canvas = Tk.Canvas(Fieldwindow, width=1500, height=900)
        canvas.grid()
        
        #labels/textfields
        canvas.create_rectangle(50, 50, 750, 750, outline='gray', fill='gray')
        lbl=Tk.Label(Fieldwindow, text="Feld Modus", fg='blue', font=("Helvetica", 60))
        lbl.place(x=800, y=75)
        lbl2=Tk.Label(Fieldwindow, text="Alle Angaben in cm", fg='blue', font=("Helvetica", 20))
        lbl2.place(x=800, y=200)
        lbl=Tk.Label(Fieldwindow, text="Feldbreite", fg='blue', font=("Helvetica", 40))
        lbl.place(x=800, y=350)
        txtw=ttk.Entry(Fieldwindow, font=("Helvetica 40"), width = 5)
        txtw.place(x=1300,y= 350)
        lbl=Tk.Label(Fieldwindow, text="Feldlänge", fg='blue', font=("Helvetica", 40))
        lbl.place(x=800, y=450)
        txtl=ttk.Entry(Fieldwindow, font=("Helvetica 40"), width = 5)
        txtl.place(x=1300,y= 450)
        lbl=Tk.Label(Fieldwindow, text="Anzahl der Einheiten", fg='blue', font=("Helvetica", 40))
        lbl.place(x=800, y=550)
        txta=ttk.Entry(Fieldwindow, font=("Helvetica 40"), width = 5)
        txta.place(x=1300,y= 550)

        #get Textfield text
        def getvalue():
            global fieldlength
            global fieldwidth
            global rotations
            global tracks
            global Anzahl
            fieldlength = int(txtl.get())
            fieldwidth = int(txtw.get())
            Anzahl = int(txta.get())
            Fieldwindow.destroy
            rotations = round(fieldlength/(pi*10.7)) # gear ratio = 1 : 3
            tracks = round(fieldwidth/23)
            x = threading.Thread(target=updatecanvas)
            x.start()
            E = threading.Thread(target=FM.runfieldmode, args = (rotations, tracks, Anzahl))
            E.start()

        
        #window setup

        fieldstart=Tk.Button(Fieldwindow, text="Start", fg='blue', font=("Helvetica", 40), command=lambda:[getvalue(), print(fieldlength, fieldwidth, rotations, tracks)])
        fieldstart.place(x=800,y=650)


        Fieldwindow.mainloop()

        #loop break
        if window.destroy:
            break

def updatecanvas():
    global coordinatesX
    global coordinatesY
    global offsetX
    global offsetY
    global upDown
    coordinatesX = [400]
    coordinatesY = [400]
    FM.positionY = 400
    gray = (128, 128, 128)
    image = Image.open(
        r"C:\Users\karst\Documents\GitHub\Lego-feldscwarm-modell\Programmierung_Lego_Feldschwarm_Modell\neue Version\Arrow.png"
    )

    resized_img = image.resize((20, 20))

    img = ImageTk.PhotoImage(resized_img, master=canvas)
    arrow = Tk.Label(Fieldwindow, image=img, bd=0)
    
    while True:
        
        if FM.speed != 0 and FM.speed != None:
            if FM.positionX + offsetX < 750 and FM.positionY + offsetY < 750 and FM.positionX + offsetX > 50 and FM.positionY + offsetY > 50:
                coordinatesX.append(FM.positionX + FM.speed / FM.mapSize *
                                    math.cos(math.radians(FM.Heading - 90)))
                coordinatesY.append(FM.positionY + FM.speed / FM.mapSize *
                                    math.sin(math.radians(FM.Heading - 90)))
                arrow.place(x=FM.positionX - 10 + offsetX, y=FM.positionY - 10 + offsetY)
                rotated_img = resized_img.rotate(FM.Heading*-1-90,
                                                 resample=Image.BICUBIC,
                                                 expand=False,
                                                 fillcolor=gray)
                img = ImageTk.PhotoImage(rotated_img, master=canvas)
                arrow.config(image=img)
                arrow.image = img
                if FM.Attachment_up:
                    canvas.create_line(
                        FM.positionX + offsetX,
                        FM.positionY + offsetY,
                        coordinatesX[len(coordinatesX) - 1] + offsetX,
                        coordinatesY[len(coordinatesY) - 1] + offsetY,
                        fill="blue")
                    upDown.append(True)
                else:
                    canvas.create_line(
                        FM.positionX + offsetX,
                        FM.positionY + offsetY,
                        coordinatesX[len(coordinatesX) - 1] + offsetX,
                        coordinatesY[len(coordinatesY) - 1] + offsetY,
                        fill="red")
                    upDown.append(False)
            else:
                arrow.place(x=10000, y=10000)



        if keyboard.is_pressed("+"):
            arrow.place(x=FM.positionX * 1.2 - 10 + offsetX,
                        y=FM.positionY * 1.2 - 10 + offsetY)
            updateMap(1.2)

            FM.mapSize /= 1.2
            arrow.place(x=FM.positionX - 10 + offsetX, y=FM.positionY - 10 + offsetY)

        if keyboard.is_pressed("-"):
            arrow.place(x=FM.positionX * 0.8 - 10 + offsetX,
                        y=FM.positionY * 0.8 - 10 + offsetY)
            updateMap(0.8)
            FM.mapSize /= 0.8
            arrow.place(x=FM.positionX - 10 + offsetX, y=FM.positionY - 10 + offsetY)
        if keyboard.is_pressed("up arrow"):
            offsetY -= 50
            updateMap(1)
            arrow.place(x=FM.positionX - 10 + offsetX, y=FM.positionY - 10 + offsetY)

        elif keyboard.is_pressed("down arrow"):
            offsetY += 50
            updateMap(1)
            arrow.place(x=FM.positionX - 10 + offsetX, y=FM.positionY - 10 + offsetY)

        elif keyboard.is_pressed("left arrow"):
            offsetX -= 50
            updateMap(1)
            arrow.place(x=FM.positionX - 10 + offsetX, y=FM.positionY - 10 + offsetY)

        elif keyboard.is_pressed("right arrow"):
            offsetX += 50
            updateMap(1)
            arrow.place(x=FM.positionX - 10 + offsetX, y=FM.positionY - 10 + offsetY)

        FM.positionX = coordinatesX[len(coordinatesX) - 1]
        FM.positionY = coordinatesY[len(coordinatesY) - 1]

        time.sleep(0.2)

def updateMap(zoomvalue):
    global coordinatesX
    global coordinatesY
    global offsetX
    global offsetY
    global upDown
    canvas.create_rectangle(50, 50, 750, 750, outline='gray', fill='gray')
    #Line = Image.open(
    #    r"C:\Users\karst\Documents\GitHub\Lego-feldscwarm-modell\Programmierung_Lego_Feldschwarm_Modell\neue Version\line_segament_.png"
    #)
    for i in range(0, len(coordinatesX)):
        coordinatesX[i] *= zoomvalue
        coordinatesY[i] *= zoomvalue
        if i != 0:
            if coordinatesX[i] + offsetX < 750 and coordinatesY[
                    i] + offsetY < 750 and coordinatesX[
                        i] + offsetX > 50 and coordinatesY[i] + offsetY > 50:
                if upDown[i]:
                    canvas.create_line(coordinatesX[i - 1] + offsetX,
                                        coordinatesY[i - 1] + offsetY,
                                        coordinatesX[i] + offsetX,
                                        coordinatesY[i] + offsetY,
                                        fill="blue")
                else:
                    canvas.create_line(coordinatesX[i - 1] + offsetX,
                                        coordinatesY[i - 1] + offsetY,
                                        coordinatesX[i] + offsetX,
                                        coordinatesY[i] + offsetY,
                                        fill="red")

def Start():
    while True:

        window1=Tk.Tk()
        
        #Labels
        lbl=Tk.Label(window1, text="Auswahl", fg='blue', font=('Helvetica', 60))
        lbl.place(x=600, y=75)
        
        #window setup
        field = Tk.Button(window1, text="Feld", fg= 'blue', font=('Helvetica',44), command = Fieldsetup)
        field.place(x=300,y=400)
        free = Tk.Button(window1, text="Frei", fg='blue', font=('Helvetica',44), command = FreeMode)
        free.place(x=1000,y=400)
        window1.title('Select')
        window1.geometry("1500x900+10+10")
        window1.configure(bg='lightgray')
        window1.update()

        #loop break
        if window1.destroy:
            break

#start
while True:
    if Zustand == 0:

        window=Tk.Tk()

        #label/Button
        lbl=Tk.Label(window, text="Willkommen", fg='blue', font=('Helvetica', 60))
        lbl.place(x=527, y=75)
        btn = Tk.Button(window, text="Start",fg = 'blue', font=('Helvetica', 44), command=lambda:[window.destroy(), Start()])
        btn.place(x = 680, y = 450)

        #window setup
        window.title('Start')
        window.geometry("1500x900+10+10")
        window.configure(bg='lightgray')
        window.mainloop()

    #loop break    
    if window.destroy:
        break
exit()