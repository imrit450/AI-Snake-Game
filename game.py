import pygame
import sys
import random
from pygame.math import Vector2
# import agent


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            # 1. We still need a rect for the positioning
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            # 2. What direction is the face heading
            if index == 0:
                # 3. Update snake direction
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]  # copy the self.body and remove the last element which is the head
            body_copy.insert(0, body_copy[0] + self.direction)  # takes the head and moves it in direction
            self.body = body_copy[:]  # returns the copied body to the original body

    def add_block(self):
        self.new_block = True

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        if head_relation == Vector2(-1, 0): self.head = self.head_right
        if head_relation == Vector2(0, 1): self.head = self.head_up
        if head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        if tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        if tail_relation == Vector2(0, 1): self.tail = self.tail_up
        if tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self):
        self.x = random.randint(1, cell_number - 1)
        self.y = random.randint(1, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        # create rectangle
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        # self.agent = AGENT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # reposition the fruit
            self.fruit.randomize()
            # add another block to the snake
            self.snake.add_block()
            # play sound
            self.snake.play_crunch_sound()

            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

    def check_fail(self):
        # check if snake is outside of the screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        # check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        print("Game Over")
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.x - 10, score_rect.y + 15))
        bg_rect = pygame.Rect(apple_rect.left - 5, apple_rect.top - 5, apple_rect.width + score_rect.width + 20,
                              apple_rect.height + 10)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

cell_size = 40
cell_number = 15
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))  # 40*20 = 800 cells
clock = pygame.time.Clock()  # influence time
apple_original = pygame.image.load('Graphics/apple.png').convert_alpha()
apple = pygame.transform.scale(apple_original, (cell_size, cell_size))
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT  # creates a user event
pygame.time.set_timer(SCREEN_UPDATE, 50)  # triggers SCREEN_UPDATE every 150 milliseconds, thus a timer

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
            print(
                "Snake Head position: " + str(main_game.snake.body[0]))
            print("Fruit Position: " + str(main_game.fruit.pos))

            # Agent Goal Based
            if main_game.snake.body[0].y < main_game.fruit.pos.y:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            elif main_game.snake.body[0].y > main_game.fruit.pos.y:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            else:
                if main_game.snake.body[0].x > main_game.fruit.pos.x:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                elif main_game.snake.body[0].x < main_game.fruit.pos.x:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))  # rgb color
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
