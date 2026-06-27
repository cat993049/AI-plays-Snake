import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4

Point = namedtuple("Point","x y")

BLOCK_SIZE = 20
SPEED = 20

WHITE=(255,255,255)
RED=(200,0,0)
BLUE=(0,0,255)
BLACK=(0,0,0)

class SnakeGame:
    def __init__(self,w=640,h=480):
        self.w=w
        self.h=h

        self.display = pygame.display.set_mode((w,h))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None,25)

        self.reset()

    def reset(self):
        self.head = Point(self.w/2,self.h/2)
        self.snake=[self.head]

        self.direction=Direction.RIGHT
        self.score=0
        self.food=None
        self._place_food()

    def _place_food(self):
        x=random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y=random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food=Point(x,y)

    def play_step(self):
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                quit()

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction=Direction.LEFT
        if keys[pygame.K_RIGHT]:
            self.direction=Direction.RIGHT
        if keys[pygame.K_UP]:
            self.direction=Direction.UP
        if keys[pygame.K_DOWN]:
            self.direction=Direction.DOWN

        self._move()
        self.snake.insert(0,self.head)

        if self._collision():
            return True,self.score

        if self.head==self.food:
            self.score+=1
            self._place_food()
        else:
            self.snake.pop()

        self._draw()
        self.clock.tick(SPEED)

        return False,self.score

    def _move(self):
        x,y=self.head.x,self.head.y

        if self.direction==Direction.RIGHT:x+=BLOCK_SIZE
        if self.direction==Direction.LEFT:x-=BLOCK_SIZE
        if self.direction==Direction.UP:y-=BLOCK_SIZE
        if self.direction==Direction.DOWN:y+=BLOCK_SIZE

        self.head=Point(x,y)

    def _collision(self):
        if self.head in self.snake[1:]:
            return True
        if self.head.x<0 or self.head.x>self.w or self.head.y<0 or self.head.y>self.h:
            return True
        return False

    def _draw(self):
        self.display.fill(BLACK)

        for p in self.snake:
            pygame.draw.rect(self.display,BLUE,pygame.Rect(p.x,p.y,BLOCK_SIZE,BLOCK_SIZE))

        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))

        text=self.font.render(str(self.score),True,WHITE)
        self.display.blit(text,(10,10))

        pygame.display.flip()