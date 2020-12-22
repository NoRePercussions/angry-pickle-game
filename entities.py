# Game entities

from __future__ import annotations
from blocks import *


class Entity:
    pos = [0, 0]  # type: list[int]
    vel = [0, 0]
    bounds = (.5, .5)
    type = "GenericEntity"
    movable = True
    collides = False
    mass = 1
    bounce = 0

    @staticmethod
    def staticEntityCollision(entity1: Entity, entity2: Entity) -> bool:
        if not entity1.collides or not entity2.collides:
            return False

        for axis in range(2):
            if not Entity.areEntitiesColliding(entity1, entity2, axis):
                return False

        entity1.onCollision(entity2)
        entity2.onCollision(entity1)

        if not entity1.movable and not entity2.movable:
            return True
            
        for axis in range(2):
            Entity.doEntityCollisionOnAxis(entity1, entity2, axis)

        return True

    def entityCollision(self: Entity, entity2: Entity) -> bool:
        return Entity.staticEntityCollision(self, entity2)

    @staticmethod
    def areEntitiesColliding(entity1: Entity, entity2: Entity, dim: int) -> bool:
        if not entity1.collides or not entity2.collides:
            return False

        bound1 = (entity1.pos[dim] - entity1.bounds[dim],
                  entity1.pos[dim] + entity1.bounds[dim])
        bound2 = (entity2.pos[dim] - entity2.bounds[dim],
                  entity2.pos[dim] + entity2.bounds[dim])

        if bound1[1] < bound2[0] \
                or bound2[1] < bound1[0]:
            return False

        return True

    @staticmethod
    def doEntityCollisionOnAxis(entity1: Entity, entity2: Entity, dim: int):
        bound1 = (entity1.pos[dim] - entity1.bounds[dim],
                  entity1.pos[dim] + entity1.bounds[dim])
        bound2 = (entity2.pos[dim] - entity2.bounds[dim],
                  entity2.pos[dim] + entity2.bounds[dim])

        if bound1[1] < bound2[0] \
                or bound2[1] < bound1[0]:
            return False

        if bound1[1] > bound2[0]:
            if entity1.movable is False:
                entity2.pos[dim] += (bound1[1] - bound2[0])
            elif entity2.movable is False:
                entity1.pos[dim] -= (bound1[1] - bound2[0])
            else:
                entity1.pos[dim] -= (bound1[1] - bound2[0]) / 2
                entity2.pos[dim] += (bound1[1] - bound2[0]) / 2
        else:
            if entity1.movable is False:
                entity2.pos[dim] -= (bound2[1] - bound1[0])
            elif entity2.movable is False:
                entity1.pos[dim] += (bound2[1] - bound1[0])
            else:
                entity2.pos[dim] -= (bound2[1] - bound1[0]) / 2
                entity1.pos[dim] += (bound2[1] - bound1[0]) / 2

        Entity.elasticEntityCollision(entity1, entity2, dim)

        return True

    @staticmethod
    def elasticEntityCollision(entity1: Entity, entity2: Entity, dim: int) -> None:
        k1 = entity1.mass * entity1.vel[dim] \
             + entity2.mass * entity2.vel[dim]

        mass = entity1.mass + entity2.mass

        new1 = (2 * k1 / mass - entity1.vel[dim]) \
               * (1 + entity2.bounce)

        new2 = (2 * k1 / mass - entity2.vel[dim]) \
               * (1 + entity1.bounce)

        entity1.vel[dim] += new1
        entity2.vel[dim] += new2

    @staticmethod
    def staticBlockCollision(entity: Entity, block: Block, blockpos: tuple[float, float]) -> bool:
        if not entity.collides or not block.collides:
            return False

        for axis in range(2):
            if not Entity.areBlockAndEntityColliding(entity, block, blockpos, axis):
                return False

        print(f"Colliding with a block at ({blockpos[0]}, {blockpos[1]})")
        block.onCollision(entity)

        if not entity.movable:
            return True

        for axis in range(2):
            Entity.doBlockCollisionOnAxis(entity, block, blockpos, axis)

        return True

    def blockCollision(self: Entity, block: Block, blockpos: tuple[float, float]) -> bool:
        Entity.staticBlockCollision(self, block, blockpos)

    @staticmethod
    def areBlockAndEntityColliding(entity: Entity, block: Block, blockpos: tuple[float, float], dim: int) -> bool:
        if not entity.collides or not block.collides:
            return False

        bound1 = (entity.pos[dim] - entity.bounds[dim],
                  entity.pos[dim] + entity.bounds[dim])
        bound2 = (blockpos[dim] - block.bounds[dim],
                  blockpos[dim] + block.bounds[dim])

        if bound1[1] < bound2[0] \
                or bound2[1] < bound1[0]:
            return False

        return True

    @staticmethod
    def doBlockCollisionOnAxis(entity: Entity, block: Block, blockpos: tuple[float, float], dim: int):
        bound1 = (entity.pos[dim] - entity.bounds[dim],
                  entity.pos[dim] + entity.bounds[dim])
        bound2 = (blockpos[dim] - block.bounds[dim],
                  blockpos[dim] + block.bounds[dim])

        if bound1[1] < bound2[0] \
                or bound2[1] < bound1[0]:
            return False

        if bound1[1] > bound2[0]:
            entity.pos[dim] -= (bound1[1] - bound2[0])
        else:
            entity.pos[dim] += (bound2[1] - bound1[0])

        Entity.elasticBlockCollision(entity, block, dim)

        return True

    @staticmethod
    def elasticBlockCollision(entity: Entity, block: Block, dim: int) -> None:

        entity.vel[dim] -= entity.vel[dim] * (1 + block.bounce)

    def doEntityMove(self: Entity) -> None:
        if not self.movable:
            return
        self.pos = [p + v for p, v in zip(self.pos, self.vel)]

    def onCollision(self: Entity, otherEntity: Entity) -> None:
        None


class Player(Entity):
    def __init__(self, source=None):
        self.type = "Player"
        self.movable = True
        self.collides = True
        self.health = 20
        self.bounds = (.5, .5)

        if source is None:
            return

        if "pos" in source.keys():
            self.pos = source['pos']
        if "vel" in source.keys():
            self.vel = source['vel']
        if "bounds" in source.keys():
            self.bounds = source['bounds']


class ScriptedEntity(Entity):
    def __init__(self, source: dict = None):
        self.path = [(0, 0)]
        self.targetVel = 1
        self.target = 0
        self.mode = "loop"
        self.direction = 1
        self.type = "ScriptedEntity"
        self.movable = False
        self.frame = 0
        self.images = []  # type: list

        if source is None:
            return

        if "path" in source.keys():
            self.path = source['path']
            self.pos = self.path[0]
        if "mode" in source.keys():
            self.mode = source['mode']
        if "type" in source.keys():
            self.type = source['type']
        if "images" in source.keys():
            self.images = source['images']
        if "numFrames" in source.keys():
            self.numFrames = source['numFrames']
        if "bounds" in source.keys():
            self.bounds = source['bounds']
        if "movable" in source.keys():
            self.movable = source['movable']
        if "mass" in source.keys():
            self.movable = source['mass']
        if "collides" in source.keys():
            self.collides = source['collides']
            if "bounce" in source.keys():
                self.bounce = source['bounce']

    def prepareEntityMove(self: Entity) -> None:
        if len(self.path) == 1:
            return

        if self.pos == self.path[self.target]:
            self.target += self.direction
            if self.target == len(self.path):
                if self.mode == "loop":
                    self.target = 0
                else:
                    self.direction = -1
                    self.target = len(self.path) - 2
            elif self.target == -1:
                self.direction = 1
                self.target = 1

        dist0 = self.path[self.target][0] - self.pos[0]
        dist1 = self.path[self.target][1] - self.pos[1]
        dist = (dist0 ** 2 + dist1 ** 2) ** .5

        self.vel[0] = self.targetVel * dist0 / dist
        self.vel[1] = self.targetVel * dist1 / dist

    def doEntityMove(self: Entity) -> None:
        if len(self.path) == 1:
            return

        self.pos = [p + v for p, v in zip(self.pos, self.vel)]
