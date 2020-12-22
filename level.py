# Level handling system

# Dimension 0 is horizontal
# Dimension 1 is vertical

from __future__ import annotations

from entities import *
from blocks import *
from PIL import Image, ImageTk
import tkinter as tk


from math import floor, ceil
import json


class Level:
    blockTypes: dict[str, Block] = {}
    entities: list[ScriptedEntity] = []
    levelmap: list[list[str]] = [[]]
    settings: dict = {}
    textures: dict = {}
    player: Player

    def readFromJSON(self: Level, path: str) -> None:
        data = Level.__readJSONFile(path)

        directory = "/".join(path.split("/")[:-1])

        self.levelmap = data['map']

        self.__parseBlocks(data['blocks'])
        self.__parseEntities(data['entities'])
        self.__parsePlayer(data['player'])
        self.__loadTextures(data['textures'], directory)

        # Todo: local settings parsing

    @staticmethod
    def __readJSONFile(path: str):
        with open(path, "r") as f:
            d = f.read()
            return json.loads(d)

    def __parseBlocks(self: Level, blockData):
        for name, data in blockData.items():
            self.blockTypes[name] = Block(data)

    def __parseEntities(self: Level, entityData):
        for entity in entityData:
            self.entities += Entity(entity)

    def __loadTextures(self, rawTextureData, directory):
        for tex, path in rawTextureData.items():
            image = Image.open(directory + "/" + path)
            image = ImageTk.PhotoImage(image)
            self.textures[tex] = image

    def __parsePlayer(self, playerData):
        self.player = Player(playerData)

    def doGameTick(self: Level):
        self.__doEntityUpdate()
        self.__doPlayerUpdate()
        self.__doEntityCollisions()
        self.__doBlockCollisions()
        self.__doMovements()

    def __doEntityUpdate(self: Level):
        for entity in self.entities:
            if abs(self.player.pos[0] - entity.pos[0]) < 20:
                entity.prepareEntityMove()

    def __doPlayerUpdate(self: Level):
        self.player.vel[1] -= -9.81/64

    def __doEntityCollisions(self: Level):
        for entity in self.entities:
            if abs(self.player.pos[0] - entity.pos[0]) < 5:
                self.player.entityCollision(entity)

    def __doBlockCollisions(self: Level):
        xPos = self.player.pos[0]
        for x in range(
                max(floor(xPos) - 2, 0),
                min(ceil(xPos) + 2, len(self.levelmap))):
            for y in range(len(self.levelmap[0])):
                if self.levelmap[x][y] is not None:
                    self.player.blockCollision(
                        self.blockTypes[self.levelmap[x][y]], (x, y))

    def __doMovements(self: Level):
        for entity in self.entities:
            if abs(self.player.pos[0] - entity.pos[0]) < 20:
                entity.doEntityMove()

        self.player.doEntityMove()

    def doRender(self: Level, canvas: tk.Canvas):
        canvas.delete('all')
        self.__drawBackdrop(canvas)
        self.__drawMap(canvas)
        self.__drawEntities(canvas)
        self.__drawPlayer(canvas)
        # Todo: UI rendering

    def __drawBackdrop(self: Level, canvas: tk.Canvas):
        if 'backdrop' in self.textures.keys():
            canvas.create_image(0, 0, image=self.textures['backdrop'])

    def __drawMap(self: Level, canvas: tk.Canvas):
        # Todo: use `block` image list
        xPos = self.player.pos[0]
        for x in range(
                max(floor(xPos) - 20, 0),
                min(ceil(xPos) + 20, len(self.levelmap))):
            for y in range(len(self.levelmap[0])):
                if self.levelmap[x][y] is not None:
                    canvas.create_image(
                        (x - self.player.pos[0]) * 64
                        + int(canvas.cget("width")) / 2 - self.textures[self.levelmap[x][y]].width() / 2,
                        (y - self.player.pos[1]) * 64
                        + int(canvas.cget("height")) / 2 - self.textures[self.levelmap[x][y]].height() / 2,
                        image = self.textures[self.levelmap[x][y]]
                    )

    def __drawEntities(self: Level, canvas: tk.Canvas):
        for entity in self.entities:
            if abs(self.player.pos[0] - entity.pos[0]) < 20:
                canvas.create_image(
                    (entity.pos[0] - self.player.pos[0])*64
                            + int(canvas.cget("width"))/2 - entity.images[entity.frame].width()/2,
                    (entity.pos[1] - self.player.pos[1])*64
                            + int(canvas.cget("height")) / 2 - entity.images[entity.frame].height()/2,
                    image = self.textures[self.images[entity.frame]]
                )
                entity.frame = (entity.frame + 1) % len(entity.images)

    def __drawPlayer(self: Level, canvas: tk.Canvas):
        playerTexture = self.textures['player']
        canvas.create_image(
            int(canvas.cget("width"))/2 - playerTexture.width()/2,
            int(canvas.cget("height"))/2 - playerTexture.height()/2,
            image = playerTexture
        )

    def processInput(self: Level, keypress: str):
        None
