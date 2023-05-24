import pygame
from pygame.math import Vector2


class Block:
    def __init__(self, pos: Vector2, width: int, height: int):
        super().__init__()
        self.position = Vector2(*pos)
        self.width = width
        self.height = height
        self.image = pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def move_to(self, pos):
        self.position = pos
        self.image = pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def move_by(self, move_vector):
        self.position += move_vector
        self.image = pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def draw(self, screen, colour):
        pygame.draw.rect(screen, colour, self.image)
        pygame.draw.rect(screen, 'black', self.image, 1)

class I_Shape(Block):
    def __init__(self, pos, width, height):
        super().__init__(pos, width, height)
        self.shape = [Block(pos, width, height), Block(pos + Vector2(width, 0), width, height),
                      Block(pos + Vector2(2 * width, 0), width, height),
                      Block(pos + Vector2(3 * width, 0), width, height)]
        self.colour = (18, 228, 228)

    def move_to(self, pos):
        vector = pos - self.position #pos relative to top left of first block.
        self.position += vector
        for block in self.shape:
            block.position += vector
            block.move_to(block.position)

    def rotate(self,quarters:int):
        center = self.shape[1].position.copy()
        for block in self.shape:
            block.position -= center  # make origin the top left corner of second block from left
            block.position = block.position.rotate(quarters*-90)  # rotate it
            block.position += center  # return origin to (0,0)
            block.move_to(block.position)
        self.position = self.shape[0].position.copy()

    def draw_shape(self, screen):
        for block in self.shape:
            block.draw(screen, self.colour)


class L_Shape(Block):
    def __init__(self, pos, width, height):
        super().__init__(pos, width, height)
        self.shape = [Block(pos, width, height),
                      Block(pos + Vector2(0, height), width, height),
                      Block(pos + Vector2(0, 2 * height), width, height),
                      Block(pos + Vector2(width, 2 * height), width, height)]
        self.move_to(pos)
        self.colour = (220, 150, 20)

    def move_to(self, pos):
        vector = pos - self.position #pos relative to top left of first block.
        self.position += vector
        for block in self.shape:
            block.position += vector
            block.move_to(block.position)

    def rotate(self,quarters:int):
        center = self.shape[3].position.copy()
        for block in self.shape:
            block.position -= center  # make origin the top left corner of bottom sticky out block in 'L'
            block.position = block.position.rotate(quarters*-90)  # rotate it
            block.position += center  # return origin to (0,0)
            block.move_to(block.position)
        self.position = self.shape[0].position.copy()

    def draw_shape(self, screen):
        for block in self.shape:
            block.draw(screen, self.colour)


class O_Shape(Block):
    def __init__(self, pos, width, height):
        super().__init__(pos, width, height)
        self.shape = [Block(pos, width, height),
                      Block(pos + Vector2(width, 0), width, height),
                      Block(pos + Vector2(0, height), width, height),
                      Block(pos + Vector2(width, height), width, height)]
        self.move_to(pos)
        self.colour = (220, 220, 20)

    def move_to(self, pos):
        vector = pos - self.position  # pos relative to top left of first block.
        self.position += vector
        for block in self.shape:
            block.position += vector
            block.move_to(block.position)

    def rotate(self,quarters:int):
        pass #rotate does nothing to a "O"


    def draw_shape(self, screen):
        for block in self.shape:
            block.draw(screen, self.colour)


class S_Shape(Block):
    def __init__(self, pos, width, height):
        super().__init__(pos, width, height)
        self.shape = [Block(pos + Vector2(width, 0), width, height),
                      Block(pos + Vector2(2 * width, 0), width, height),
                      Block(pos + Vector2(width, height), width, height),
                      Block(pos + Vector2(0, height), width, height)]
        self.move_to(pos)
        self.colour = (20, 220, 20)

    def move_to(self, pos):
        vector = pos - self.position  # pos relative to top left of first block.
        self.position += vector
        for block in self.shape:
            block.position += vector
            block.move_to(block.position)

    def rotate(self,quarters:int):
        center = self.shape[2].position.copy()
        for block in self.shape:
            block.position -= center  # make origin the top left corner bottom right block of S shape
            block.position = block.position.rotate(quarters*-90)  # rotate it
            block.position += center  # return origin to (0,0)
            block.move_to(block.position)
        self.position = self.shape[0].position.copy()

    def draw_shape(self, screen):
        for block in self.shape:
            block.draw(screen, self.colour)


class T_Shape(Block):
    def __init__(self, pos, width, height):
        super().__init__(pos, width, height)
        self.shape = [Block(pos, width, height),
                      Block(pos + Vector2(width, 0), width, height),
                      Block(pos + Vector2(2 * width, 0), width, height),
                      Block(pos + Vector2(width, height), width, height)]
        self.move_to(pos)
        self.colour = (220, 20, 220)

    def move_to(self, pos):
        vector = pos - self.position  # pos relative to top left of first block.
        self.position += vector
        for block in self.shape:
            block.position += vector
            block.move_to(block.position)

    def rotate(self,quarters:int):
        center = self.shape[3].position.copy()
        for block in self.shape:
            block.position -= center  # make origin the top left corner of bottom block in 'T'
            block.position = block.position.rotate(quarters*-90)  # rotate it
            block.position += center  # return origin to (0,0)
            block.move_to(block.position)
        self.position = self.shape[0].position.copy()

    def draw_shape(self, screen):
        for block in self.shape:
            block.draw(screen, self.colour)
