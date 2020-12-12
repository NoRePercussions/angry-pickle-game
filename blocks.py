# Game block handling

from __future__ import annotations
from entities import *


class Block:
    # Todo: dict reader

    def __init__(self, source=None):
        self.frame = 0
        self.bounds = (32, 32)
        self.images = []
        self.collides = False
        self.bounce = 0

        if source is None: return

        if "bounds" in source.keys():
            self.bounds = source['bounds']
        if "images" in source.keys():
            self.images = source['images']
        if "collides" in source.keys():
            self.collides = source['collides']
        if "bounce" in source.keys():
            self.bounce = source['bounce']
