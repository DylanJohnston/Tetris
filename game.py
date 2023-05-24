import random
import sys

import pygame
from pygame.math import Vector2

import shapes

pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

pygame.mixer.music.load("Tetris.mp3")
pygame.mixer.music.play(-1)

top_left_of_grid = Vector2(50, 50)
grid_width, grid_height = (40, 40)
top_left_of_next_block_box = Vector2(525, 150)
next_block_box_width, next_block_box_height = (200, 200)
num_columns = 10
num_rows = 15

game_font = pygame.font.Font(size=40)


def game_text():
    next_block_text = str("Next Block:")
    text_surface = game_font.render(next_block_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(topleft=(top_left_of_next_block_box.x, top_left_of_next_block_box.y - 50))
    screen.blit(text_surface, text_rect)


class Main:

    def __init__(self):  # groups
        self.bg = pygame.image.load('blueBG.png')
        self.reset()
        # self.score = 0
        # self.next_shape = [self.create_new_shape(top_left_of_next_block_box, grid_width, grid_height)]
        # self.current_shape = []
        # self.placed_blocks = []
        # self.block_direction = 0
        # self.block_speed = 1
        # self.quarters_to_rotate = 0
        # self.game_over = False

    # noinspection PyMethodMayBeStatic
    def create_new_shape(self, position: Vector2, width, height):
        tetromino_shapes = ['I', 'L', 'O', 'S', 'T']
        index = random.randint(0, len(tetromino_shapes)-1)
        return eval(f"shapes.{tetromino_shapes[index]}_Shape({position + Vector2(25, 25)},{width},{height})")

    def equip_new_block(self):
        if not self.current_shape:
            for the_shape in self.next_shape:
                new_position = Vector2(top_left_of_grid.x + 3 * grid_width, top_left_of_grid.y)
                the_shape.move_to(new_position)
                self.current_shape.append(the_shape)
                self.next_shape.remove(the_shape)
                self.next_shape.append(self.create_new_shape(top_left_of_next_block_box, grid_width, grid_height))

    def set_direction(self, direction):
        self.block_direction = direction

    def move_current_block(self):
        at_the_left_edge = False
        at_the_right_edge = False
        for the_shape in self.current_shape:
            # first, check if shape is at either edge
            for block in the_shape.shape:
                if block.position.x <= top_left_of_grid.x:
                    at_the_left_edge = True
                elif block.position.x >= top_left_of_grid.x + grid_width * (num_columns - 1):
                    at_the_right_edge = True
            # if direction and edge give invalid move, set direction = 0 so block falls straight down
            if (at_the_left_edge and self.block_direction == -1) or (at_the_right_edge and self.block_direction == 1):
                self.block_direction = 0
            move_to_position = the_shape.position + Vector2(self.block_direction * grid_width, grid_height)
            the_shape.move_to(move_to_position)

    def check_collisions(self):
        for shape in self.current_shape:
            collide = False
            bottomed = False
            up_amount = -1
            for block in shape.shape:
                if block.position in [list(placed.position) for placed, _ in self.placed_blocks]:
                    while (block.position + Vector2(0, grid_height * up_amount)
                           in [list(placed.position) for placed, _ in self.placed_blocks]):
                        up_amount -= 1
                    collide = True
                elif block.position.y > top_left_of_grid.y + (num_rows - 1) * grid_height:
                    bottomed = True
            if collide or bottomed:
                for block in shape.shape:
                    block.move_by(Vector2(0, up_amount * grid_height))

                if not self.block_direction and not self.quarters_to_rotate:
                    for block in shape.shape:
                        self.placed_blocks.append((block, shape.colour))
                    self.current_shape.remove(shape)

    def check_lines(self):
        for i in range(num_rows):
            complete_line = True  # True until proven False
            for ele in [[top_left_of_grid.x + grid_width * j, top_left_of_grid.y + grid_height * i] for j in
                        range(num_columns)]:
                if ele not in [elem.position for elem, _ in self.placed_blocks]:
                    complete_line = False
                    break
            if complete_line:
                self.score += 1
                for ele in ([[top_left_of_grid.x + grid_width * j, top_left_of_grid.y + grid_height * i]
                             for j in range(num_columns)]):
                    index = [block.position for block, _ in self.placed_blocks].index(ele)
                    del self.placed_blocks[index]
                for block, _ in self.placed_blocks:
                    if block.position.y < top_left_of_grid.y + grid_height * i:
                        block.position += Vector2(0, grid_height)
                        block.image = pygame.Rect(block.position.x, block.position.y, grid_width, grid_height)

    def update(self):
        if self.quarters_to_rotate:
            for shape in self.current_shape:
                shape.rotate(self.quarters_to_rotate)
                self.quarters_to_rotate = 0
        else:
            for _ in range(self.block_speed):
                self.move_current_block()
                self.check_collisions()
        self.check_collisions()
        self.check_game_over()
        if self.game_over:
            self.reset()
        self.check_lines()
        self.equip_new_block()
        self.block_speed = 1
        self.block_direction = 0

    def score_text(self):
        score_text = str(f"Score: {self.score}")
        score_text_surface = game_font.render(score_text, True, (0, 0, 0))
        score_text_rect = score_text_surface.get_rect(
            topleft=(top_left_of_next_block_box.x, top_left_of_next_block_box.y + 300))
        screen.blit(score_text_surface, score_text_rect)

    def check_game_over(self):
        for block,_ in self.placed_blocks:
            if block.position.y < top_left_of_grid.y:
                self.game_over = True

    def reset(self):
        self.score = 0
        self.next_shape = [self.create_new_shape(top_left_of_next_block_box, grid_width, grid_height)]
        self.current_shape = []
        self.placed_blocks = []
        self.block_direction = 0
        self.block_speed = 1
        self.quarters_to_rotate = 0
        self.game_over = False

    def draw_all(self, the_screen):
        for shape in self.current_shape + self.next_shape:
            shape.draw_shape(the_screen)
        for block, colour in self.placed_blocks:
            block.draw(the_screen, colour)


SCREEN_UPDATE = pygame.USEREVENT
game_speed = 500
pygame.time.set_timer(SCREEN_UPDATE, game_speed)
main_game = Main()
score_checker = 0

while True:

    updates_this_frame = 0

    if main_game.score > score_checker:
        game_speed -= 20
        if game_speed < 100:
            game_speed = 100
        pygame.time.set_timer(SCREEN_UPDATE, 0)
        pygame.time.set_timer(SCREEN_UPDATE, game_speed)
        score_checker = main_game.score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                pass
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                main_game.block_speed = 3
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                main_game.block_direction = -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                main_game.block_direction = 1
            if event.key == pygame.K_PAGEUP or event.key == pygame.K_q:
                main_game.quarters_to_rotate = 1
            if event.key == pygame.K_PAGEDOWN or event.key == pygame.K_e:
                main_game.quarters_to_rotate = -1

        if event.type == SCREEN_UPDATE and updates_this_frame == 0:
            main_game.update()
            updates_this_frame += 1

    screen.blit(main_game.bg, (0, 0))
    pygame.draw.rect(screen, 'black',
                     pygame.Rect(top_left_of_grid.x, top_left_of_grid.y, grid_width * 10, grid_height * 15))
    pygame.draw.rect(screen, 'black', pygame.Rect(top_left_of_next_block_box.x, top_left_of_next_block_box.y,
                                                  next_block_box_width, next_block_box_height))
    main_game.draw_all(screen)
    main_game.score_text()
    game_text()
    pygame.display.update()
    clock.tick(60)
