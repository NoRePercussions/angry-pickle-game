# Todo: general config
# Todo: global setting
# Todo: game tick cycle
# Todo: render process
# Todo: sounds + music
# Todo: make graphics

from entities import *
from blocks import *

# Todo: keypresses are weird!
# If using key pressed hooks:
# os.system('xset r off') at start
# os.system('xset r on') at end

# use `import keyboard`
#     `if keyboard.is_pressed('b'):`


x = Entity()
x.vel[0] = 5
y = Entity()
y.bounce = 1
y.pos[0] = 70
y.vel[0] = -5

x.entityCollision(y, 0)
x.doEntityMove()
y.doEntityMove()
x.entityCollision(y, 0)

print(x.pos, y.pos)
print(x.vel, y.vel)