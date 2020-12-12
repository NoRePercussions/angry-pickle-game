# Platformer Level Editor

import map
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
window = tk.Tk()

def init():
    #drawWelcomeScreen()
    window.filename="/Users/tuckershea/Documents/testmap/testmap.json"
    drawLevelEditor()

def drawWelcomeScreen():
    clearall()
    greeting = tk.Label(
        text="Welcome to the level editor!",
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

def drawLevelEditor():
    clearall()
    window.geometry("1500x400")
    header = tk.Frame(window)

    tk.Label(header,
        text=window.filename.split("/")[-1],
        fg="black",
        font=("Arial", 20)).grid(row=0, column=0, columnspan=1)

    levelmap = map.Map()
    levelmap.readMapFromFile(window.filename)
    print(levelmap.dir)

    drawnLevel = tk.Frame(window)

    def redraw():
        clearall(drawnLevel)
        drawLevel(drawnLevel, levelmap)
        drawnLevel.pack()

    tk.Button(header,
        text="Remove row from top",
        fg="black",
        width=24,
        font=("Arial", 20),
        command=sequence(levelmap.remTop, redraw)
        ).grid(row=0, column=1)
    tk.Button(header,
        text="Add row to top",
        fg="black",
        width=24,
        font=("Arial", 20),
        command=sequence(levelmap.addTop, redraw)
        ).grid(row=0, column=2)
    tk.Button(header,
        text="Remove row from bottom",
        fg="black",
        width=24,
        font=("Arial", 20),
        command=sequence(levelmap.remBottom, redraw)
        ).grid(row=1, column=1)
    tk.Button(header,
        text="Add row to bottom",
        fg="black",
        width=24,
        font=("Arial", 20),
        command=sequence(levelmap.addBottom, redraw)
        ).grid(row=1, column=2)

    tk.Button(header,
        text="Remove column from left",
        fg="black",
        width=24,
        font=("Arial", 20),
        command=sequence(levelmap.remLeft, redraw)
        ).grid(row=1, column=3)
    tk.Button(header,
        text="Add column to left",
        fg="black",
        width=24,
        font=("Arial", 20),
        command=sequence(levelmap.addLeft, redraw)
        ).grid(row=0, column=3)
    tk.Button(header,
        text="Remove column from right",
        fg="black",
        width=24,
        font=("Arial", 20),
        command=sequence(levelmap.remRight, redraw)
        ).grid(row=1, column=4)
    tk.Button(header,
        text="Add column to right",
        fg="black",
        width=24,
        font=("Arial", 20),
        command=sequence(levelmap.addRight, redraw)
        ).grid(row=0, column=4)

    header.grid_columnconfigure(3, weight=1)
    header.grid_rowconfigure(1, weight=1)

    header.pack()

    redraw()

    print("abcd")
    window.mainloop()

def drawLevel(levelframe, level):
    canvas = tk.Canvas(levelframe, width=64, height=64)
    selectedicon = None
    levelobj = [[None]*level.height]*level.width

    def setSelected(x,y):
        levelframe.selx = x
        levelframe.sely = y
        outline = Image.open(level.dir + "/outline.png")
        render = ImageTk.PhotoImage(outline)
        img = tk.Label(levelframe, text="", image=render)
        img.image = render
        #img.grid(row=x, column=y+1)
        print(x,y+1)
        for widget in levelframe.winfo_children():
            info = widget.grid_info()
            print(info)
            if len(info) > 0 and info["row"]==str(x) and info["column"]==str(y+1):
                widget["highlightthickness"] = 2
                widget["highlightbackground"] = "#000000"

                print("aaaaaaa")
                #img.grid(row=x,column=y+1)

    for row in range(level.height):
        load = Image.open(level.dir + "/arrow.jpg")
        load = load.resize((64, 64))
        render = ImageTk.PhotoImage(load)
        img = tk.Label(levelframe, text="abcd", image=render)
        img.image = render
        img.grid(row=row, column=0)

    for col in range(level.width):
        for row in range(level.height):
            if level.levelmap[col][row] is None or level.textures[level.levelmap[col][row]["type"]] is None:
                load = Image.new("RGB", (64,64), (255, 255, 255))
            else:
                load = Image.open(level.dir + "/" + level.textures[level.levelmap[col][row]["type"]])
                load = load.resize((64,64))
            render = ImageTk.PhotoImage(load)
            img = tk.Button(levelframe, text="abcd", image=render, command=caller(setSelected, row, col))
            img["borderwidth"] = 0
            img.image = render
            img.grid(row=row, column=col+1)
            levelobj[col][row] = img


def clearall(frame=window):
    for widget in frame.winfo_children():
        widget.destroy()

def sequence(*functions):
    def func(*args, **kwargs):
        return_value = None
        for function in functions:
            return_value = function(*args, **kwargs)
        return return_value
    return func

def caller(f, a, b):
    def func(*args, **kwargs):
        f(a, b)
    return func

init()