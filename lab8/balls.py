from ctypes import pointer
import pygame
from pygame.draw import *
from random import randint
from tkinter import *
from random import randrange as rnd, choice
import time



pygame.init()

FPS = 2
screen = pygame.display.set_mode((1000, 700))

points = 0
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    '''рисует новый шарик '''
    global x, y, r
    x = randint(200, 800)
    y = randint(200, 700)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

    
def click(event):
    x0 = event.pos[0]
    y0  = event.pos[1]
    if (y0 - y)**2 + (x0 - x)**2 <= r**2:
        print('+')
    else:
        print('-')
    if (y0 - y)**2 + (x0 - x)**2 <= r**2:
        points += 1
    

def print_points(point):
    font = pygame.font.Font(None, 25)
    text = font.render("Score: "+str(point),True, GREEN)
    screen.blit(text, [10,10])


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    new_ball()
    print_points(points)
    pygame.display.update()
    #screen.fill(BLACK)

pygame.quit()