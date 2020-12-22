# Game block handling

from __future__ import annotations
from entities import *


class Block:
    def __init__(self, source: dict =None):
        self.frame = 0
        self.bounds = (.5, .5)
        self.images = []
        self.collides = True
        self.bounce = 0

        if source is None:
            return

        if "bounds" in source.keys():
            self.bounds = source['bounds']
        if "images" in source.keys():
            self.images = source['images']
        if "collides" in source.keys():
            self.collides = source['collides']
        if "bounce" in source.keys():
            self.bounce = source['bounce']

    def onCollision(self: Block, entity: Entity):
        None
