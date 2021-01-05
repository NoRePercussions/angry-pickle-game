# Todo: sounds + music

from entities import *
from blocks import *
from level import *
from keymonitor import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from time import sleep

# ~980 LOC

#file = "/Users/tuckershea/Downloads/angry-pickle-game/testmap/testmap.json"
# testing code for Anwyn
def drawWelcomeScreen():
    greeting = tk.Label(
        text="Welcome to the angry pickle game!",
        width=30,
        fg="black",
        font=("Arial", 44))
    greeting.pack()

    def openFileSelector():
        window.filename = filedialog.askopenfilename(initialdir = "~/Documents",title = "Select file",
                                                 filetypes = (("json files","*.json"),("all files","*.*")))
        filebutton.setvar("text", window.filename)
        if window.filename not in ("", None):
            gobutton.pack()


    filebutton = tk.Button(text="Select File",
                           command = openFileSelector,
                           font=("Arial", 24),
                           fg="black",
                           height=2)
    var = tk.IntVar(0)
    gobutton = tk.Button(text="Continue",
                           command = lambda: var.set(1),
                           font=("Arial", 24),
                           fg="black",
                           height=2)
    filebutton.pack()
    window.lift()
    gobutton.wait_variable(var)

window = tk.Tk()
window.geometry("1024x768")

# Todo: let Level bind to km
km = KeyMonitor()
km.bindToWindow(window)

drawWelcomeScreen()
for widget in window.winfo_children():
    widget.destroy()

c = tk.Canvas(window, width=1024, height=768)
c.pack()

mylevel = Level()
mylevel.readFromJSON(window.filename)

while True:
    mylevel.processInput(km)
    mylevel.doGameTick()
    mylevel.doRender(c)
    window.update_idletasks()
    window.update()
    sleep(.01)

window.mainloop()
