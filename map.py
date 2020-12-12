# Level handler
# by Tucker Shea
# Dec 5 2020

import json

class Map:
    data = None
    levelmap = None
    textures = None
    dir = ""
    screenWidth = 10

    def __init__(self):
        None

    def readMapFromFile(self, fileName):
        with open(fileName, "r") as f:
            d = f.read()
            self.data = json.loads(d)
        self.levelmap = self.data['map']
        self.textures = self.data['textures']
        self.dir = "/".join(fileName.split("/")[:-1])

        self.update()

    def update(self):
        self.width = len(self.levelmap)
        self.height = len(self.levelmap[0])

    def getSolidBlocks(self):
        return [[j if j.type == "block" else [] for j in i] for i in self.levelmap]

    def getEnemies(self):
        return [[j if j.type == "enemy" else [] for j in i] for i in self.levelmap]

    def returnLocalMap(self, x=0):
        assert x < len(self.levelmap), "x coordinate must be within the map"
        start = max(0, x - self.screenWidth)
        end   = min(len(self.levelmap), x + self.screenWidth)
        return self.levelmap[start, end]

    def remTop(self):
        self.levelmap = [i[1:] for i in self.levelmap]
        self.update()

    def addTop(self):
        self.levelmap = [[None]+i for i in self.levelmap]
        self.update()

    def remBottom(self):
        self.levelmap = [i[:-1] for i in self.levelmap]
        self.update()

    def addBottom(self):
        self.levelmap = [i+[None] for i in self.levelmap]
        self.update()

    def remLeft(self):
        self.levelmap = self.levelmap[1:]
        self.update()

    def addLeft(self):
        self.levelmap = [[None] * self.height] + self.levelmap
        self.update()

    def remRight(self):
        self.levelmap = self.levelmap[:-1]
        self.update()

    def addRight(self):
        self.levelmap = self.levelmap + [[None] * self.height]
        self.update()