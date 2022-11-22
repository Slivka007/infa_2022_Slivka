import math
import pygame
import threading
from random import choice, randint
from abc import abstractmethod, ABCMeta
from itertools import product

# max fps
FPS = 30
# some colors
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
# screen sizes
WIDTH = 800
HEIGHT = 600


class Movable(metaclass=ABCMeta):
    """Describes a movable object"""
    x = 0
    y = 0
    vx = 0
    vy = 0

    @abstractmethod
    def move(self):
        """Moves object"""
        pass


class Drawable(metaclass=ABCMeta):
    """Describes a drawable object"""
    screen = None
    color = None

    @abstractmethod
    def draw(self):
        """Draws object"""
        pass


class Shell(Movable, Drawable, metaclass=ABCMeta):
    """Describes shell"""
    r = 0

    @abstractmethod
    def hittest(self, obj):
        """Checks if this shell crosses obj
        Args:
            obj - instance of Target
        Returns:
            True if this shell crosses obj, else False
        """
        pass


class Target(Movable, Drawable, metaclass=ABCMeta):
    """Describes a target"""

    @abstractmethod
    def __init__(self, screen):
        """Constructor of Target class
        Args:
            screen - pygame surface, on which target is drawn
        """
        pass


class PierchingShell(Shell, metaclass=ABCMeta):
    """Describes a pierching shell (hits target on crossing)"""

    def move(self, t=1):
        """Moves object
        Args:
            t = 1 - proportionately velocity of movement
        """
        # get time to achieve horizontal and vertical borders
        tx = (WIDTH - self.x - self.r) / self.vx if self.vx > 0 else (
            -(self.x - self.r) / self.vx if self.vx != 0 else WIDTH)
        ty = -(HEIGHT - self.y - self.r) / self.vy if self.vy < 0 else (
            (self.y - self.r) / self.vy if self.vy != 0 else HEIGHT)

        # if they are too big, move linearly
        if t < min(tx, ty):
            self.x += self.vx * t
            self.y -= self.vy * t
            self.vy -= t
            return

        # move to border and reflect
        if tx < ty:
            # firstly achieves horizontal border
            self.x += self.vx * tx
            self.y -= self.vy * tx
            self.vy -= tx
            self.vx = -self.vx
            self.move(t - tx)
        else:
            # firstly achieves vertical border
            self.x += self.vx * ty
            self.y -= self.vy * ty
            self.vy -= ty
            self.vy = -self.vy
            self.move(t - ty)

    def draw(self):
        """Draws a target"""
        pygame.draw.circle(
            self.screen, self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        # check crossing with circle objects
        if isinstance(obj, Circle) or isinstance(obj, Bomb) or isinstance(obj, Gun):
            return math.hypot(self.x - obj.x, self.y - obj.y) <= self.r + obj.r
        # check crossing with square objects
        if isinstance(obj, Square):
            return any([abs(point[0] - self.x) < self.r and abs(point[1] - self.y) < self.r
                        for point in product([obj.x + obj.r / 2, obj.x - obj.r / 2],
                                             [obj.y + obj.r / 2, obj.y - obj.r / 2])]) or \
                   (abs(self.x - obj.x) < obj.r and abs(self.y - obj.y) < (obj.r + self.r) / 2) or \
                   (abs(self.y - obj.y) < obj.r and abs(self.x - obj.x) < (obj.r + self.r) / 2)


class CaliberShell(PierchingShell):
    """Describes a caliber shell (big and slow)"""

    def __init__(self, screen: pygame.Surface, x, y):
        """ CaliberShell constructor

        Args:
            screen - pygame surface, on which target is drawn
            x - x coordinate
            y - y coordinate
        """
        # surface
        self.screen = screen
        # x coordinate
        self.x = x
        # y coordinate
        self.y = y
        # radius
        self.r = 10
        # x velocity
        self.vx = 0
        # y velocity
        self.vy = 0
        # color
        self.color = choice(GAME_COLORS)


class SubCaliberShell(PierchingShell):
    """Describes SubCaliberShell (small and fast)"""

    def __init__(self, screen: pygame.Surface, x, y):
        """ SubCaliberShell constructor

        Args:
            screen - pygame surface, on which target is drawn
            x - x coordinate
            y - y coordinate
        """
        # surface
        self.screen = screen
        # x coordinate
        self.x = x
        # y coordinate
        self.y = y
        # radius
        self.r = 5
        # x velocity
        self.vx = 0
        # y velocity
        self.vy = 0
        # color
        self.color = choice(GAME_COLORS)


class Gun(Target, metaclass=ABCMeta):
    """Describes gun"""

    def __init__(self, screen):
        """Gun constructor"""
        # shell list
        self.shells = [CaliberShell, SubCaliberShell]
        # surface
        self.screen = screen
        # power
        self.f2_power = 1
        # is powered
        self.f2_on = 0
        # direction
        self.ax = 1
        self.ay = 0
        # color
        self.color = GREY
        # coordinates
        self.x = randint(0, WIDTH)
        self.y = randint(0, HEIGHT)
        # radius
        self.r = 20
        # velocity
        self.vx = 1
        self.vy = 1

    def fire2_start(self, event):
        """Starts fire"""
        self.f2_on = 1

    def fire2_end(self, event):
        """Shoots

        Causes on mouse up
        Start coordinate and velocity values depend on mouse position
        """
        global shells
        # add shell
        new_shell = self.shells[randint(0, 1)](self.screen, self.x, self.y)
        new_shell.x += (self.r + new_shell.r + 10) * self.ax / math.hypot(self.ax, self.ay)
        new_shell.y += (self.r + new_shell.r + 10) * self.ay / math.hypot(self.ax, self.ay)
        new_shell.r += 5
        new_shell.vx = self.f2_power * self.ax / math.hypot(self.ax, self.ay)
        new_shell.vy = - self.f2_power * self.ay / math.hypot(self.ax, self.ay)
        if isinstance(new_shell, SubCaliberShell):
            new_shell.vx *= 1.5
            new_shell.vy *= 1.5
        shells.append(new_shell)
        # reset f2_on and f2_power
        self.f2_on = 0
        self.f2_power = 10

    @abstractmethod
    def targetting(self, obj):
        """Targeting"""
        pass

    def draw(self):
        pygame.draw.line(self.screen, self.color, (self.x, self.y),
                         (self.x + self.f2_power * self.ax / math.hypot(self.ax, self.ay),
                          self.y + self.f2_power * self.ay / math.hypot(self.ax, self.ay)), 5)
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r)

    def power_up(self):
        """Increases power of shell"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class UserGun(Gun):
    """Describes user's gun (user moves it and shoots by mouse and """

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y - self.r > 0:
            self.y -= self.vy
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y + self.r < HEIGHT:
            self.y += self.vy
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x + self.r < WIDTH:
            self.x += self.vx
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x - self.r > 0:
            self.x -= self.vx

    def targetting(self, event):
        """Targeting, depends on mouse position"""
        # set direction
        if event:
            self.ax = event.pos[0] - self.x
            self.ay = event.pos[1] - self.y
        # set color
        if self.f2_on:
            # targetins
            self.color = RED
        else:
            # not targeting
            self.color = GREY


class ComputerGun(Gun):
    """Describes gun """

    def move(self):
        pass

    def targetting(self, pos):
        """Targets on pos
        Args:
            pos - tuple (x, y) of target coordinates
        """
        # set direction
        self.ax = pos[0] - self.x
        self.ay = pos[1] - self.y

    def shoot(self):
        """Shoots to user gun"""

        # shoot function
        def _shoot():
            self.color = RED
            self.fire2_start(None)
            for _ in range(randint(10, 20)):
                self.power_up()
            self.fire2_end(None)
            self.color = GREY

        # shoot in new thread
        t = threading.Thread(target=_shoot)
        t.daemon = True
        t.start()


class Circle(Target):
    """Describes circle target (moves along line, reflects from borders)"""

    def __init__(self, screen):
        """Circle constructor
        Args:
            screen - pygame surface
        """
        # surface
        self.screen = screen
        # coordinates
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        # velocity
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        # radius
        self.r = randint(2, 50)
        # color
        self.color = RED

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        # move
        self.x += self.vx
        self.y -= self.vy
        # reflect from right border
        if self.x + self.r > WIDTH:
            self.x = 2 * (WIDTH - self.r) - self.x
            self.vx = -self.vx
        # reflect from left border
        if self.x - self.r < 0:
            self.x = 2 * self.r - self.x
            self.vx = -self.vx
        # reflect from bottom border
        if self.y + self.r > HEIGHT:
            self.y = 2 * (HEIGHT - self.r) - self.y
            self.vy = -self.vy
        # reflect from top border
        if self.y - self.r < 0:
            self.y = 2 * self.r - self.y
            self.vy = -self.vy


class Square(Target):
    """Describes square target (stays, oscillating)"""

    def __init__(self, screen):
        """Square constructor
        Args:
            screen - pygame surface
        """
        # surface
        self.screen = screen
        # coordinates
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        # oscillation velocity
        self.v = 0
        # mean radius
        self.R = 50
        # radius
        self.r = self.R + randint(1, 10)
        # color
        self.color = BLUE

    def draw(self):
        pygame.draw.rect(
            self.screen,
            self.color,
            (self.x - self.r / 2, self.y - self.r / 2, self.r, self.r),
            self.r
        )

    def move(self):
        # change velocity
        self.v -= self.r - self.R
        # change radius
        self.r += int(self.v * randint(1001, 1100) / 1000)


class Bomb(Target):
    """Describes bomb target (stays, on hit spawns 2 targets)"""

    def __init__(self, screen):
        """Bomb constructor
        Args:
            screen - pygame surface
        """
        # surface
        self.screen = screen
        # coordinate
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        # radius
        self.r = 20
        # color
        self.color = BLACK

    def move(self):
        pass

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


# score counter
score = 0
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# flying shells list
shells = []
# guns number
GUNS = 2
# computer guns
guns = [ComputerGun(screen) for _ in range(GUNS)]
# user's gun
gun = UserGun(screen)
# spawning target types
TARGET_TYPES = [Circle, Square, Bomb]
# min of targets
TARGETS = 2
# targets list
targets = [TARGET_TYPES[randint(0, 2)](screen) for _ in range(TARGETS)]
# append guns to targets
targets.append(gun)
targets.extend(guns)


def mouse_button_down_event_handler(event):
    """MOUSEBUTTONDOWN event handler"""
    gun.fire2_start(event)


def mouse_button_up_event_handler(event):
    """MOUSEBUTTONUP event handler"""
    gun.fire2_end(event)


def mouse_motion_event_handler(event):
    """MOUSEMOTION event handler"""
    gun.targetting(event)


finished = False

while not finished:
    screen.fill(WHITE)
    # move and draw each target
    for target in targets:
        target.move()
        target.draw()
    # move and draw each shell
    for b in shells:
        b.move()
        b.draw()
    pygame.display.update()
    clock.tick(FPS)

    # in random moment shoot from one gun
    if randint(0, 300) == 0:
        idx = randint(0, 1)
        guns[idx].targetting((gun.x, gun.y))
        guns[idx].shoot()

    # process events
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                finished = True
            case pygame.MOUSEBUTTONDOWN:
                mouse_button_down_event_handler(event)
            case pygame.MOUSEBUTTONUP:
                mouse_button_up_event_handler(event)
            case pygame.MOUSEMOTION:
                mouse_motion_event_handler(event)

    # process hits
    for shell in shells:
        for target in targets:
            # if hit something
            if shell.hittest(target):
                # if hit yourself, quit
                if target == gun:
                    finished = True
                    print("Hit you")
                    break
                # spawn target
                targets.append(TARGET_TYPES[randint(0, 2)](screen))
                # if hit bomb. spawn more targets
                if isinstance(target, Bomb):
                    for _ in range(2):
                        targets.append(TARGET_TYPES[randint(0, 2)](screen))
                # remove hit target
                targets.remove(target)
                # remove shell
                shells.remove(shell)
                # increase score
                score += 1
                break
    gun.power_up()

pygame.quit()