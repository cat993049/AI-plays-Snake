import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x y')

BLOCK_SIZE = 20
SPEED = 40

WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)

class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((w,h))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 30)

        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w//2, self.h//2)

        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - 2*BLOCK_SIZE, self.head.y)
        ]

        self.food = None
        self.frame_iteration = 0
        self.score = 0
        self.history = set()

        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)

        if self.food in self.snake:
            self._place_food()

    def get_state(self):
        head = self.snake[0]

        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)

        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        state = [
            # danger straight
            (dir_r and self.is_collision(point_r)) or
            (dir_l and self.is_collision(point_l)) or
            (dir_u and self.is_collision(point_u)) or
            (dir_d and self.is_collision(point_d)),

            # right
            (dir_u and self.is_collision(point_r)) or
            (dir_d and self.is_collision(point_l)) or
            (dir_l and self.is_collision(point_u)) or
            (dir_r and self.is_collision(point_d)),

            # left
            (dir_u and self.is_collision(point_l)) or
            (dir_d and self.is_collision(point_r)) or
            (dir_l and self.is_collision(point_d)) or
            (dir_r and self.is_collision(point_u)),

            # direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # food location
            self.food.x < head.x,
            self.food.x > head.x,
            self.food.y < head.y,
            self.food.y > head.y
        ]

        return np.array(state, dtype=int)

    def play_step(self, action):
        self.frame_iteration += 1

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0
        done = False

        # 💀 morir
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            return -10, True, self.score

        # 🍎 comida
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 🔥 reward por acercarse a comida
        dist_old = abs(self.head.x - self.food.x) + abs(self.head.y - self.food.y)

        if self.head in self.history:
            reward -= 5
        else:
            self.history.add(self.head)

        self._update_ui()
        self.clock.tick(SPEED)

        return reward, False, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for p in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(p.x,p.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(p.x+4,p.y+4,12,12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))

        text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, (10,10))

        pygame.display.flip()

    def _move(self, action):
        clock = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock.index(self.direction)

        if np.array_equal(action,[1,0,0]):
            new_dir = clock[idx]
        elif np.array_equal(action,[0,1,0]):
            new_dir = clock[(idx+1)%4]
        else:
            new_dir = clock[(idx-1)%4]

        self.direction = new_dir

        x,y = self.head.x, self.head.y

        if self.direction == Direction.RIGHT: x += BLOCK_SIZE
        elif self.direction == Direction.LEFT: x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN: y += BLOCK_SIZE
        elif self.direction == Direction.UP: y -= BLOCK_SIZE

        self.head = Point(x,y)

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        if pt.x < 0 or pt.x >= self.w or pt.y < 0 or pt.y >= self.h:
            return True

        if pt in self.snake[1:]:
            return True

        return False