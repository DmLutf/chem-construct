# -*- coding: utf-8 -*-

import pygame
pygame.init()

WIN_SIZE = (700, 700)
win = pygame.display.set_mode(WIN_SIZE, pygame.RESIZABLE)

text = pygame.font.Font("Calibri.ttf", 24)
header = pygame.font.Font("Calibri.ttf", 48)


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


class Menu:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.color = (210, 210, 210)

        self.buttons = []
        self.labels = []

    def draw(self):
        pygame.draw.rect(win, self.color,
                         (self.x, self.y, self.w, self.h))

        for label in self.labels:
            label.draw((self.x, self.y))

        k = 0
        for i in self.buttons:
            for button in i:
                button.draw((self.x, self.y + k))
                k += 70

    def resize(self, new_h):
        self.h = new_h

    def update(self, event):
        global popup
        
        if not popup:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.buttons:
                    for button in i:
                        button.react()

        if event.type == pygame.VIDEORESIZE:
            self.resize(event.h)

        for i in self.buttons:
            for button in i:
                button.select((self.x, self.y))


class Viewport:
    def __init__(self, x, y, w, h, bg):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.bg = bg

        self.molecules = []

    def draw(self):
        pygame.draw.rect(win, self.bg,
                         (self.x, self.y, self.w, self.h))

        for molecule in self.molecules:
            molecule.draw()

    def resize(self, new_w, new_h):
        self.w = new_w
        self.h = new_h

    def update(self, event):
        global popup

        if not popup:
            pass
        
        if event.type == pygame.VIDEORESIZE:
            self.resize(event.w, event.h)


class Popup:
    def __init__(self, w, h,
                 buttons, labels, inputs):
        self.x = (WIN_SIZE[0] - w) // 2
        self.y = (WIN_SIZE[1] - h) // 2

        self.w = w
        self.h = h

        self.color = (210, 210, 210)

        self.buttons = buttons
        self.labels = labels
        self.inputs = inputs

        self.bg = pygame.Surface((WIN_SIZE[0], WIN_SIZE[1])).set_alpha(200)
        self.bg.fill(self.color)

    def draw(self):
        win.blit(self.bg, (0, 0))

        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

        for button in self.buttons:
            button.draw((self.x, self.y))

        for label in self.labels:
            label.draw((self.x, self.y))

        for inpuut in self.inputs:
            inpuut.draw((self.x, self.y))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.react()

            for inpuut in self.inputs:
                inpuut.react((self.x, self.y))

        if event.type == pygame.VIDEORESIZE:
            self.resize(event.w, event.h)

        for button in self.buttons:
            button.select((self.x, self.y))

    def resize(self, new_w, new_h):
        self.bg = pygame.Surface((new_w, new_h)).set_alpha(200)
        self.bg.fill(self.color)


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

    def select(self, offset):
        pos = pygame.mouse.get_pos()

        if pos[0] > self.x + offset[0] and pos[0] < self.x + self.w + offset[0]:
            if pos[1] > self.y + offset[1] and pos[1] < self.y + self.h + offset[1]:
                self.selected = True

            else:
                self.selected = False

        else:
            self.selected = False

    def react(self):
        if self.selected:
            if self.arg:
                self.func(self.arg)
            else:
                self.func()


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
    for event in pygame.event.get():
        update(event)

        menu.update(event)

        viewport.update(event)

        if popup:
            popup.update(event)

def redrawWindow():
    viewport.draw()

    menu.draw()

    if popup:
        popup.draw()

    pygame.display.update()

def update(event):
    global done
    
    if event.type == pygame.QUIT:
        done = True
    
    if event.type == pygame.VIDEORESIZE:
        WIN_SIZE = (event.w, event.h)
        win = pygame.display.set_mode(WIN_SIZE, pygame.RESIZABLE)




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
    
    menu.buttons.insert(0, [Button(10, 160, menu.w - 20, 60,
                                   viewport.molecules[len(viewport.molecules) - 1].name, moleculeOptions, 
                                   viewport.molecules[len(viewport.molecules) - 1].index)])

    menu.buttons[0].append([Button(30, 160, menu.w - 40, 60,
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

menu = Menu(0, 0, 400, WIN_SIZE[1])
menu.labels.append(Label(0, 0, menu.w, 150, "Список молекул", header,
                         (255, 255, 255), (0, 0, 0)))

menu.buttons.append([Button(10, 160, menu.w - 20, 60,
                            "Создать молекулу", createMolecule)])

popup = None

done = False
while not done:
    checkEvents()

    redrawWindow()

pygame.quit() 
