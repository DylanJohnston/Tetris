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

class Shape(Block):
    def __init__(self, type, pos, width, height):
        super().__init__(pos, width, height)
        if type == 'I':
            self.shape = [Block(pos, width, height), Block(pos + Vector2(width, 0), width, height),
                          Block(pos + Vector2(2 * width, 0), width, height),
                          Block(pos + Vector2(3 * width, 0), width, height)]
            self.colour = (18, 228, 228)
            self.width = 4
            self.height = 1
            self.rotation_center_block = 1
        elif type == 'L':
            self.shape = [Block(pos, width, height),
                          Block(pos + Vector2(0, height), width, height),
                          Block(pos + Vector2(0, 2 * height), width, height),
                          Block(pos + Vector2(width, 2 * height), width, height)]
            self.colour = (220, 150, 20)
            self.width = 2
            self.height = 3
            self.rotation_center_block = 3

        elif type == 'O':
            self.shape = [Block(pos, width, height),
                          Block(pos + Vector2(width, 0), width, height),
                          Block(pos + Vector2(0, height), width, height),
                          Block(pos + Vector2(width, height), width, height)]
            self.colour = (220, 220, 20)
            self.width = 2
            self.height = 2
            self.rotation_center_block = 3

        elif type == 'S':
            self.shape = [Block(pos + Vector2(width, 0), width, height),
                          Block(pos + Vector2(2 * width, 0), width, height),
                          Block(pos + Vector2(width, height), width, height),
                          Block(pos + Vector2(0, height), width, height)]
            self.colour = (20, 220, 20)
            self.width = 3
            self.height = 2
            self.rotation_center_block = 2

        elif type == 'T':
            self.shape = [Block(pos, width, height),
                          Block(pos + Vector2(width, 0), width, height),
                          Block(pos + Vector2(2 * width, 0), width, height),
                          Block(pos + Vector2(width, height), width, height)]
            self.move_to(pos)
            self.colour = (220, 20, 220)
            self.width = 3
            self.height = 2
            self.rotation_center_block = 3

    def move_to(self, pos):
        vector = pos - self.position  # pos relative to top left of first block.
        self.position += vector
        for block in self.shape:
            block.position += vector
            block.move_to(block.position)

    def rotate(self, quarters: int):
        if type == 'O':
            pass
        else:
            center = self.shape[self.rotation_center_block].position.copy()
            for block in self.shape:
                block.position -= center  # make origin the top left corner of second block from left
                block.position = block.position.rotate(quarters * -90)  # rotate it
                block.position += center  # return origin to (0,0)
                block.move_to(block.position)
            self.position = self.shape[0].position.copy()

    def draw_shape(self, screen):
        for block in self.shape:
            block.draw(screen, self.colour)
