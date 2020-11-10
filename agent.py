import pygame
import game
from pygame.math import Vector2


class AGENT:
    def __init__(self, fruit_position, cell_size, cell_number, snake_head, direction, snake_body):
        self.state = {
            "game_over" : False,
            "change_position": Vector2(),
            "current_position": Vector2(snake_head),
            "current_size": [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)],
            "previous_size": [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)],
            "score":0

        }

        self.direction = {
            "right" : Vector2(1,0),
            "left": Vector2(-1,0),
            "up": Vector2(0,-1),
            "down": Vector2(0,1)
        }
        self.fruit_position = fruit_position
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.snake_head = snake_head
        self.direction = direction
        self.snake_body = snake_body


    def state_game_over(self):
        if not 0 <= self.snakeBody[0].x < self.cell_number or not 0 <= self.snake_body[0].y < self.cell_number:
            self.state["game_over"] = True

    def action_move_right(self):
        if state_change_position:




    def moveSnake(self, snakeBody,snakeDirection, fruitPosition):
        if snakeBody[0].y < fruitPosition.y:
            if snakeDirection.y != -1:
                snake = Vector2(0, 1)
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
