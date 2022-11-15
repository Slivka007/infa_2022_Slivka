import math
from random import choice
from random import randint
import pygame


FPS = 30
DELTA_TIME = 1/FPS*10

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

GRAVITY = 10

class Game:
    balls = {}
    targets = {}
    score = 0
    id_counter = 0
    new_ball_timer = 0
    def __init__(self, screen, gun, clock, font_style) -> None:
        self.screen = screen
        self.clock = clock
        self.font_style = font_style
        self.gun = gun

class Ball:
    def __init__(self, screen: pygame.Surface, id, x=40, y=450) -> None:
        """ 
        Args:
        x - start horizontal position,
        y - start vertical posotion
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self) -> None:
        """Move ball"""
        self.is_on_edge()
        self.vy -= GRAVITY * DELTA_TIME
        self.x += self.vx * DELTA_TIME
        self.y -= self.vy * DELTA_TIME

    def is_on_edge(self) -> None:
        """Collision handing"""
        if (self.x + self.r > WIDTH):
            self.x = WIDTH - self.r        
            self.vx = -self.vx
        elif (self.x - self.r < 0):
            self.x = self.r
            self.vx = -self.vx
        if (self.y + self.r > HEIGHT):
            self.y = HEIGHT - self.r
            self.vy = -self.vy
        elif (self.y -self.r < 0):
            self.y = self.r
            self.vy = -self.vy
    def draw(self) -> None:
        """Ball render"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj) -> bool:
        """Collision handing.

        Args:
            obj: Object to check for collision.
        Returns:
            True if objects collide, else False
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + self.r) ** 2:
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 30
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.rect(
            self.screen,
            YELLOW,
            (0, 450, 40,10)

        )
        pygame.draw.circle(
            self.screen,
            self.color,
            (10,10),
            10
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    points = 0
    live = 1

    def __init__(self, screen):       
        self.screen = screen
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = RED
        self.draw

    def new_target(self):
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = RED
        self.draw

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target):
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()