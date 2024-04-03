from tkinter import *
import tkinter as tk
import tkinter.ttk
import tkinter.font
import os

window = Tk()
window.title("check box test")

def status1_print():
    print(CheckVar1.get())

def status2_print():
    print(CheckVar2.get())

CheckVar1=IntVar()
CheckVar2=IntVar()

c1=Checkbutton(window,text="Music",variable=CheckVar1, command=status1_print)
c2=Checkbutton(window,text="Video",variable=CheckVar2, command=status2_print)

c1.pack()
c2.pack()

window.geometry('800x500+220+200')
window.mainloop()