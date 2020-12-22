# Todo: general config
# Todo: global setting
# Todo: sounds + music
# Todo: make graphics

from entities import *
from blocks import *
from level import *
import tkinter as tk
from PIL import Image, ImageTk
from time import sleep

# Todo: keypresses are weird!
# If using key pressed hooks:
# os.system('xset r off') at start
# os.system('xset r on') at end

# use `import keyboard`
#     `if keyboard.is_pressed('b'):`

# Todo: change <= to < in collision check
# Todo: implement backwards collision checking for reflections
# Todo: idk what this was supposed to be but probably collision related

file = "/Users/tuckershea/Documents/testmap/testmap.json"

window = tk.Tk()
window.geometry("832x384")

c = tk.Canvas(window, width=832, height=384)
c.pack()

mylevel = Level()
mylevel.readFromJSON(file)

for i in range(6):
    mylevel.doGameTick()
    print(mylevel.player.pos)
    print(mylevel.levelmap)
    mylevel.doRender(c)
    window.update_idletasks()
    window.update()
    sleep(1)

window.mainloop()
