# -*- coding: utf-8 -*-

import pygame
pygame.init()

WIN_SIZE = (900, 500)
win = pygame.display.set_mode(WIN_SIZE, pygame.RESIZABLE)

text = pygame.font.Font("Calibri.ttf", 24)
header = pygame.font.Font("Calibri.ttf", 48)

clock = pygame.time.Clock()


class ElementsList:
    def __init__(self, path):
        self.path = path

    def openFile(self):
        table = open(self.path, "r")
        
        self.list = table.read().split("\n")
        
        for i in range(len(self.list)):
            self.list[i] = self.list[i].split()
            
            for j in range(len(self.list[i])):
                try:
                    self.list[i][j] = int(self.list[i][j])
                    
                except:
                    pass
        
        table.close()


class TableButton:
    def __init__(self, x, y, name, color,
                 protons, neutrons, electrons):
        self.x = x
        self.y = y

        self.w = 100
        self.h = 60
        
        self.name = name
        self.color = color

        self.protons = protons
        self.neutrons = neutrons
        self.electrons = electrons
        
        self.selected = False

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

        writeText(self.name, (self.x + 5, self.y + 5), (0, 0, 0), text)

    def createAtom(self, parent):
        parent.atoms.append(Atom(0, 0,
                                 self.protons, self.neutrons, self.electrons,
                                 self.name, self.color,
                                 parent))
        
    def checkEvents(self):
        pos = pygame.mouse.get_pos()
        
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                self.selected = True


class Viewport:
    def __init__(self, x, y, w, h, bg_color):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.bg_color = bg_color

        self.molecules = []

    def draw(self):
        pygame.draw.rect(win, self.bg_color,
                         (self.x, self.y, self.w, self.h))

        for molecule in self.molecules:
            molecule.draw()

    def changeSize(self, width, height):
        self.w = width
        self.h = height


class Menu:
    def __init__(self):
        self.x = 0
        self.y = 0
        
        self.w = 400
        self.h = WIN_SIZE[1]

        self.color = (210, 210, 210)

        self.mbuttons = []
        self.abuttons = []
        
        self.labels = []

    def draw(self):
        pygame.draw.rect(win, self.color,
                         (self.x, self.y, self.w, self.h))

        for label in self.labels:
            label.draw((self.x, self.y))

        for button in self.mbuttons:
            button.draw((self.x, self.y))

    def changeSize(self, height):
        self.h = height


class Popup:
    def __init__(self, w, h, buttons, labels, inputs):
        self.w = w
        self.h = h

        self.color = (210, 210, 210)

        self.buttons = buttons
        self.labels = labels
        self.inputs = inputs

        self.bg = pygame.Surface((WIN_SIZE[0], WIN_SIZE[1]))
        self.bg.fill(self.color)
        self.bg.set_alpha(200)

    def draw(self):
        size = self.bg.get_size()
        
        win.blit(self.bg, (0, 0))

        pygame.draw.rect(win, self.color, ((size[0] - self.w) // 2,
                                           (size[1] - self.h) // 2,
                                           self.w, self.h))

        for button in self.buttons:
            button.draw(((size[0] - self.w) // 2,
                         (size[1] - self.h) // 2))

        for label in self.labels:
            label.draw(((size[0] - self.w) // 2,
                        (size[1] - self.h) // 2))

        for inputb in self.inputs:
            inputb.draw(((size[0] - self.w) // 2,
                         (size[1] - self.h) // 2))

    def changeSize(self, width, height):
        self.bg = pygame.Surface((width, height))
        self.bg.fill(self.color)
        self.bg.set_alpha(200)


class Button:
    def __init__(self, x, y, w, h, text, func, arg=None):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.func = func

        self.color = (240, 240, 240)
        self.text = text
        
        self.selected = False
        
        self.arg = arg

    def draw(self, offset):
        if not self.selected:
            color = self.color
        else:
            color = (self.color[0] + 15,
                     self.color[1] + 15,
                     self.color[2] + 15)
            
        pygame.draw.rect(win, color, (self.x + offset[0], self.y + offset[1],
                                      self.w, self.h))

        writeText(self.text, (self.x +
                              (self.w - len(self.text) * 12) // 2 + offset[0],
                              self.y + (self.h - 24) // 2 + offset[1]),
                  (0, 0, 0), text)

    def checkSelect(self, offset):
        pos = pygame.mouse.get_pos()

        if pos[0] > self.x + offset[0] and pos[0] < self.x + self.w + offset[0]:
            if pos[1] > self.y + offset[1] and pos[1] < self.y + self.h + offset[1]:
                self.selected = True

            else:
                self.selected = False

        else:
            self.selected = False


class Label:
    def __init__(self, x, y, w, h,
                 text, font,
                 bg_color, fg_color):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.text = text
        self.font = font

        self.bg_color = bg_color
        self.fg_color = fg_color

    def draw(self, offset):
        pygame.draw.rect(win, self.bg_color,
                         (self.x + offset[0], self.y + offset[1],
                          self.w, self.h))

        if self.font == header:
            size = 24
        else:
            size = 12
        
        writeText(self.text,
                  (self.x + (self.w - len(self.text) * size) // 2 + offset[0],
                   self.y + (self.h - size * 2) // 2 + offset[1]),
                  self.fg_color, self.font)


class InputBox:
    def __init__(self, x, y, w, h,
                 fg_color, bg_color,
                 font):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.fg_color = fg_color
        self.bg_color = bg_color

        self.font = font
        self.text = "aaaa"

        self.selected = False

    def draw(self, offset):
        if self.selected:
            color = (self.bg_color[0] + 5,
                     self.bg_color[1] + 5,
                     self.bg_color[2] + 5)
        else:
            color = self.bg_color
        
        pygame.draw.rect(win, color,
                         (self.x + offset[0], self.y + offset[1],
                          self.w, self.h))

        writeText(self.text, (self.x + offset[0] + 12,
                              self.y + (self.h - 24) // 2 + offset[1]),
                  self.fg_color, self.font)
        
    def checkSelect(self, offset):
        pos = pygame.mouse.get_pos()
        
        if pos[0] > self.x + offset[0] and pos[0] < self.x + self.w + offset[0]:
            if pos[1] > self.y + offset[1] and pos[1] < self.y + self.h + offset[1]:
                self.selected = True
            
            else:
                self.selected = False
        
        else:
            self.selected = False


class Molecule:
    def __init__(self, name, index):
        self.name = name
        self.index = index

        self.atoms = []
        self.cons = []

    def draw(self):
        for conn in self.cons:
            conn.draw((self.x, self.y))
        
        for atom in self.atoms:
            atom.draw((self.x, self.y))


class Atom:
    def __init__(self, x, y,
                 protons, neutrons, electrons,
                 name, color,
                 parent):
        self.x = x
        self.y = y

        self.r = 10

        self.protons = protons
        self.neutrons = neutrons
        self.electrons = electrons

        self.name = name
        self.color = color
        
        self.parent = parent

    def draw(self, offset):
        pygame.draw.circle(win, self.color, (self.x + offset[0], self.y + offset[1]), self.r)
        writeText(self.name, (self.x - 4 + offset[0], self.y + offset[1] - 4), (0, 0, 0), text)


class Connection:
    def __init__(self, atom1, atom2):
        self.x1 = atom1.x
        self.y1 = atom1.y

        self.x2 = atom2.x
        self.y2 = atom2.y

        self.w = 10

    def draw(self, offset):
        pygame.draw.aaline(win, (230, 230, 230),
                           (self.x1 + offset[0], self.y1 + offset[1]),
                           (self.x2 + offset[0], self.y2 + offset[1]),
                           self.w)


def writeText(text, coords, color, font):
    img = font.render(text, True, color)
    win.blit(img, coords)

def checkEvents():
    global done, popup, WIN_SIZE

    if not popup:
        for button in menu.mbuttons:
            button.checkSelect((menu.x,
                                menu.y + (len(menu.mbuttons) - 1 - menu.mbuttons.index(button)) * 75))

    else:
        for button in popup.buttons:
            button.checkSelect(((WIN_SIZE[0] - popup.w) // 2,
                                (WIN_SIZE[1] - popup.h) // 2))
        
        for inputb in popup.inputs:
            inputb.checkSelect(((WIN_SIZE[0] - popup.w) // 2,
                                (WIN_SIZE[1] - popup.h) // 2))        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.VIDEORESIZE:
            WIN_SIZE = (event.w, event.h)

            viewport.changeSize(WIN_SIZE[0], WIN_SIZE[1])
            menu.changeSize(WIN_SIZE[1])
            
            if popup:
                popup.changeSize(WIN_SIZE[0], WIN_SIZE[1])

            win = pygame.display.set_mode(WIN_SIZE, pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not popup:
                    for button in menu.mbuttons:
                        if button.selected:
                            if button.arg != None:
                                button.func(button.arg)
                            else:
                                button.func()

                else:
                    for button in popup.buttons:
                        if button.selected:
                            if button.arg != None:
                                button.func(button.arg)
                            else:
                                button.func()

def redrawWindow():
    win.fill((0, 0, 0))

    viewport.draw()

    menu.draw()

    if popup:
        popup.draw()

    pygame.display.update()




def closePopup():
    global popup
    popup = None

def moleculeOptions(index):
    global popup

    popup = Popup(800, 600, 
                  [Button(350, 530, 100, 60,
                          "0K", nameMolecule, index),

                   Button(10, 250, 200, 40,
                          "Удалить молекулу", deleteMolecule, index)], 
                  
                  [Label(0, 0, 800, 150, 
                         "Настройки молекулы", header, 
                         (0, 0, 0), (255, 255, 255)),
                   
                   Label(10, 160, 200, 40, 
                         "Название:", text,
                         (210, 210, 210), (0, 0, 0))],
                  
                  [InputBox(220, 160, 570, 40,
                            (0, 0, 0), (190, 190, 190), 
                            text)])

def createMolecule():
    viewport.molecules.append(Molecule("", len(viewport.molecules)))
    
    moleculeOptions(len(viewport.molecules) - 1)
    
    menu.mbuttons.append(Button(10, 160, menu.w - 20, 60,
                                viewport.molecules[len(viewport.molecules) - 1].name, moleculeOptions, 
                                viewport.molecules[len(viewport.molecules) - 1].index))

    menu.abuttons.append([Button(30, 160, menu.w - 40, 60,
                                 "Создать атом", createAtom,
                                 viewport.molecules[len(viewport.molecules) - 1].index)])

def deleteMolecule(index):
    for i in range(index + 1, len(viewport.molecules)):
        viewport.molecules[i].index -= 1
        menu.mbuttons[i + 1].arg -= 1
    
    viewport.molecules.pop(index)
    menu.mbuttons.pop(index + 1)

    closePopup()

def nameMolecule(index):
    viewport.molecules[index].name = "Молекула " + str(index + 1)
    menu.mbuttons[index + 1].text = viewport.molecules[index].name
    
    closePopup()

def createAtom(parent):
    print(a)




elements = ElementsList("elements.txt")
elements.openFile()

viewport = Viewport(0, 0, WIN_SIZE[0], WIN_SIZE[1], (0, 0, 0))

menu = Menu()
menu.labels.append(Label(0, 0, menu.w, 150, "Список молекул", header,
                         (255, 255, 255), (0, 0, 0)))

menu.mbuttons.append(Button(10, 160, menu.w - 20, 60,
                            "Создать молекулу", createMolecule))

popup = None

done = False
while not done:
    clock.tick(60)

    checkEvents()

    redrawWindow()

pygame.quit()
