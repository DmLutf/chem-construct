from math import *

import pygame
pygame.init()

WIN_SIZE = (700, 700)
win = pygame.display.set_mode(WIN_SIZE)

clock = pygame.time.Clock()

G_CONST = 1


class Particle:
    def __init__(self, x, y, r, m, charge, color):
        self.x = x
        self.y = y

        self.r = r
        
        self.m = m
        self.charge = charge

        self.vel = [0, 0]
        self.angle = 0

        self.color = color

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)

    def move(self):
        self.x += self.vel[0]
        self.y += self.vel[1]

    def interact(self, part):
        self.angle = atan2(self.y - part.y, self.x - part.x)
        
        dist = sqrt((self.x - part.x)**2 + (self.y - part.y)**2)
        force = (part.m / self.m) * G_CONST / (dist / 25)**2

        self.vel[0] += force * cos(self.angle) * part.charge * self.charge
        self.vel[1] += force * sin(self.angle) * part.charge * self.charge


def checkEvents():
    global done

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    proton.interact(electron)
    proton.interact(electron2)
    proton.move()

    electron.interact(proton)
    electron.interact(electron2)
    electron.move()

    electron2.interact(proton)
    electron2.interact(electron)
    electron2.move()

def redrawWindow():
    win.fill((0, 0, 0))

    proton.draw()
    
    electron.draw()
    electron2.draw()

    pygame.display.update()

proton = Particle(300, 300, 20, 2, 1, (255, 0, 0))

electron = Particle(300, 550, 10, 0.05, -1, (0, 0, 255))
electron.vel = [6.35, 0]

electron2 = Particle(300, 50, 10, 0.05, -1, (0, 0, 255))
electron2.vel = [-6.35, 0]

done = False
while not done:
    clock.tick(60)

    checkEvents()

    redrawWindow()

pygame.quit()
