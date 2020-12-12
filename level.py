# Level handling system

from __future__ import annotations

from entities import *
from blocks import *
from PIL import Image


from math import floor, ceil
import json


class Level:
    blockTypes: dict[str, Block]
    entities: list[Entity]
    map: list[list[str]]
    settings: dict
    textures: dict[str, str]
    player: Player

    def readFromJSON(self: Level, path: str) -> None:
        data = Level.__readJSONFile(path)

        directory = "/".join(path.split("/")[:-1])

        self.map = data['map']

        self.__parseBlocks(data['btypes'])
        self.__parseEntities(data['entities'])
        self.__parsePlayer(data['player'])
        self.__loadTextures(data['textures'], directory)

        # Todo: local setting parsing

    @staticmethod
    def __readJSONFile(path: str):
        with open(path, "r") as f:
            d = f.read()
            return json.loads(d)

    def __parseBlocks(self: Level, blockData):
        for name, data in blockData:
            self.blockTypes[name] = Block(data)

    def __parseEntities(self: Level, entityData):
        for entity in entityData:
            self.entities += Entity(entity)

    def __loadTextures(self, rawTextureData, directory):
        for tex, path in rawTextureData:
            image = Image.open(directory + "/" + path)
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
        None

    def __doEntityCollisions(self: Level):
        for entity in self.entities:
            if abs(self.player.pos[0] - entity.pos[0]) < 5:
                self.player.entityCollision(entity)

    def __doBlockCollisions(self: Level):
        xPos = self.player.pos[0]
        for x in range(floor(xPos)-2, ceil(xPos)+2):
            for y in range(len(self.map[0])):
                self.player.blockCollision(
                    self.blockTypes[self.map[x][y]], (x, y))

    def __doMovements(self: Level):
        for entity in self.entities:
            if abs(self.player.pos[0] - entity.pos[0]) < 20:
                entity.doEntityMove()

        self.player.doEntityMove()

    def doRender(self):
        None
        # Todo: literally all graphics
        # render backdrop
        # prepare and render map
        # prepare and render entities
        # render player
        # UI rendering done by game.py