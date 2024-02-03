#LIBRARIES
from math import *

import pygame
pygame.init()

#WINDOW CONFIGURATION
WIN_SIZE = (800, 800)
win = pygame.display.set_mode(WIN_SIZE)

#OTHER VARIABLES
font = pygame.font.SysFont("arial", 32)

#CONSTANTS
DEF_R = 50


#CLASSES
class Atom:
    def __init__(self, x, y, r, color, name):
        self.x = x
        self.y = y

        self.r = r
        self.color = color

        self.name = name

        self.selected = False
        self.pressed = False

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)
        write_text(self.name,
                   (self.x - 10 * len(self.name), self.y - 18),
                   (255, 255, 255))

        '''if self.pressed:
            pygame.draw.circle(win, (200, 200, 200),
                               (self.x, self.y), self.r + 3, 4)'''

    def select(self):
        pos = pygame.mouse.get_pos()

        if sqrt((pos[0] - self.x)**2 + (pos[1] - self.y)**2) <= self.r:
            self.selected = True
        else:
            self.selected = False

    def press(self):
        if pygame.mouse.get_pressed()[0]:
            if self.selected:
                self.pressed = True
        else:
            self.pressed = False

    def move(self):
        global rel
        
        if self.pressed:
            self.x += rel[0]
            self.y += rel[1]


class Connection:
    def __init__(self, atom1, atom2, n):
        self.atom1 = atom1
        self.atom2 = atom2

        self.n = n

        self.w = 30
        self.l = 80

    def draw(self):
        pygame.draw.line(win, (220, 220, 220), (self.atom1.x, self.atom1.y),
                         (self.atom2.x, self.atom2.y), self.w)


#FUNCTIONS
def write_text(text, coords, color):
    img = font.render(text, True, color)
    win.blit(img, coords)

def check_events():
    global done, rel

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #for conn in connections:
    
    for atom in atoms:
        atom.select()
        atom.press()
        atom.move()

    rel = pygame.mouse.get_rel()

def redraw_window():
    win.fill((0, 0, 0))

    for conn in connections:
        conn.draw()
    
    for atom in atoms:
        atom.draw()

    pygame.display.update()

#PREPARATIONS
atoms = [Atom(600, 400, DEF_R, (255, 0, 0), "C"),
         Atom(500, 300, DEF_R - 10, (0, 255, 0), "H")]

connections = [Connection(atoms[0], atoms[1], 1)]

rel = (0, 0)

#MAINLOOP
done = False
while not done:
    check_events()

    redraw_window()

pygame.quit()
