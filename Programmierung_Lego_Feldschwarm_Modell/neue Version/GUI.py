from cmath import pi
from doctest import master
from operator import truediv
from pydoc import text
import string
from tkinter import *
from turtle import window_width
import turtle
import Free
import FieldMode
import Test
from webbrowser import get
import keyboard
from tkinter import ttk
from tkinter import Canvas


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

#def Stop():
#    Free.running = False

def testmode():
    while TRUE:
        Test.Testrun()

def FreeMode():
    while TRUE:
        Free.Freerun()

def Fieldsetup():
    while TRUE:

        Fieldwindow=Tk()
        
        #labels/textfields
        lbl=Label(Fieldwindow, text="Feld Modus", fg='blue', font=("Helvetica", 60))
        lbl.place(x=600, y=75)
        lbl2=Label(Fieldwindow, text="Alle Angaben in cm", fg='blue', font=("Helvetica", 20))
        lbl2.place(x=600, y=200)
        lbl=Label(Fieldwindow, text="Feldbreite", fg='blue', font=("Helvetica", 40))
        lbl.place(x=100, y=350)
        txtw=ttk.Entry(Fieldwindow, font=("Helvetica 40"))
        txtw.place(x=600,y= 350)
        lbl=Label(Fieldwindow, text="Feldlänge", fg='blue', font=("Helvetica", 40))
        lbl.place(x=100, y=450)
        txtl=ttk.Entry(Fieldwindow, font=("Helvetica 40"))
        txtl.place(x=600,y= 450)
        lbl=Label(Fieldwindow, text="Anzahl der Einheiten", fg='blue', font=("Helvetica", 40))
        lbl.place(x=100, y=550)
        txta=ttk.Entry(Fieldwindow, font=("Helvetica 40"))
        txta.place(x=600,y= 550)

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
            rotations = round(fieldlength/(pi*10.7)) # gear ratio = 0.333 : 1 
            tracks = round(fieldwidth/23)
            FieldMode.runfieldmode(rotations, tracks, Anzahl)
        
        #window setup
        fieldstart=Button(Fieldwindow, text="Start", fg='blue', font=("Helvetica", 40), command=lambda:[getvalue(), print(fieldlength, fieldwidth, rotations, tracks)])
        fieldstart.place(x=600,y=700)
        Fieldwindow.title('FieldMode')
        Fieldwindow.geometry("1500x900+10+10")
        Fieldwindow.configure(bg='lightgray')
        Fieldwindow.mainloop()

        #loop break
        if window.destroy:
            break


def Start():
    while True:

        window1=Tk()
        
        #Labels
        lbl=Label(window1, text="Auswahl", fg='blue', font=('Helvetica', 60))
        lbl.place(x=600, y=75)
        
        #window setup
        field = Button(window1, text="Feld", fg= 'blue', font=('Helvetica',44), command=Fieldsetup)
        field.place(x=300,y=400)
        free = Button(window1, text="Frei", fg='blue', font=('Helvetica',44), command=FreeMode)
        free.place(x=1000,y=400)
        
        test = Button(window1, text="Test", fg='blue', font=('Helvetica',44), command=testmode)
        test.place(x=650,y=550)
        window1.title('Select')
        window1.geometry("1500x900+10+10")
        window1.configure(bg='lightgray')
        window1.mainloop()

        #loop break
        if window.destroy:
            break

#start
while True:
    if Zustand == 0:

        window=Tk()

        #label/Button
        lbl=Label(window, text="Willkommen", fg='blue', font=('Helvetica', 60))
        lbl.place(x=527, y=75)
        btn = Button(window, text="Start",fg = 'blue', font=('Helvetica', 44), command=lambda:[window.destroy(), Start()])
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