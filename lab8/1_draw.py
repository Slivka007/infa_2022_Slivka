import pygame
import pygame.draw  as pgd


FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((255, 0, 0))


pgd.circle(screen, (255, 255, 0), (200, 175), 150)
pgd.circle(screen, (0, 0, 0), (200, 175), 150, 1)
pgd.circle(screen, (255, 0, 0), (130, 130), 30)
pgd.circle(screen, (0, 0, 0), (130, 130), 30, 1)
pgd.circle(screen, (0, 0, 0), (130, 130), 15)
pgd.circle(screen, (255, 0, 0), (260, 130), 25)
pgd.circle(screen, (0, 0, 0), (260, 130), 25, 1)
pgd.circle(screen, (0, 0, 0), (260, 130), 12.5)
pygame.draw.rect(screen, (0, 0, 0), 
                 (130, 250, 150, 20))


pygame.draw.line(screen, (0, 0, 0), 
                 [70, 30], 
                 [185, 130], 20)

pygame.draw.line(screen, (0, 0, 0), 
                 [225, 108], 
                 [360, 50], 20)

'''
pygame.draw.line(screen, (0, 0, 0), 
                 [100, 20], 
                 [167, 146], 10)
                 '''

#pgd.circle(screen, (0, 255, 0), (200, 175), 50)
#pgd.circle(screen, (255, 255, 255), (200, 175), 50, 5)

pygame.init()
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()