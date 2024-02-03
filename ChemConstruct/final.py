# -*- coding: utf-8 -*-

#MODULES
import math

import pygame
pygame.init()

#WINDOW
WIN_SIZE = (900, 500)
win = pygame.display.set_mode(WIN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("ChemConstruct")

#FONTS
header = pygame.font.Font("Calibri.ttf", 48)
normal = pygame.font.Font("Calibri.ttf", 24)

#CLASSES
class Label:
    def __init__(self, x, y, w, h,
                 bg, fg, text, font):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.bg = bg
        self.fg = fg

        self.text = text
        self.font = font

    def draw(self, offset):
        size = self.font.size(self.text)
        
        pygame.draw.rect(win, self.bg, (self.x + offset[0], self.y + offset[1],
                                        self.w, self.h))

        write_text(self.text, self.font, self.fg,
              (self.x + (self.w - size[0]) // 2 + offset[0],
               self.y + (self.h - size[1]) // 2 + offset[1]))


class Button:
    def __init__(self, x, y, w, h,
                 bg, fg, text, func, arg=None, contour=False):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.bg = bg
        self.fg = fg

        self.text = text

        self.func = func
        self.arg = arg

        self.selected = False

        self.contour = contour

    def draw(self, offset):
        size = normal.size(self.text)

        if self.selected:
            color = (self.bg[0] + 15,
                     self.bg[1] + 15,
                     self.bg[2] + 15)
        else:
            color = self.bg
        
        pygame.draw.rect(win, color, (self.x + offset[0],
                                      self.y + offset[1],
                                      self.w, self.h))

        if self.contour:
            pygame.draw.rect(win, (255, 255, 255), (self.x + offset[0],
                                                    self.y + offset[1],
                                                    self.w, self.h), 3)

        write_text(self.text, normal, self.fg,
              (self.x + (self.w - size[0]) // 2 + offset[0],
               self.y + (self.h - size[1]) // 2 + offset[1]))

    def click(self):
        if self.arg:
            self.func(self.arg)
        else:
            self.func()


class Menu:
    def __init__(self, w, color, buttons, labels):
        self.x = 0
        self.y = 0

        self.w = w
        self.h = WIN_SIZE[1]

        self.color = color

        self.buttons = buttons
        self.labels = labels

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

        for button in self.buttons:
            button.draw((self.x, self.y))

        for label in self.labels:
            label.draw((self.x, self.y))

    def update_height(self, new_h):
        self.h = new_h

    def update_buttons_y(self):
        offset = 160

        for i in range(len(self.buttons) - 1, -1, -1):
            self.buttons[i].y = offset

            offset += 70


class Atom:
    def __init__(self, x, y, r, color, name):
        self.x = x
        self.y = y

        self.r = r

        self.color = color
        self.name = name

        self.connections = []

        self.moved = False
        self.highlight = False

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x + camera.x, self.y + camera.y), self.r)

        size = header.size(self.name)
        
        write_text(self.name, header, (255, 255, 255),
              (self.x - self.r + (2 * self.r - size[0]) // 2 + camera.x,
               self.y - self.r + (2 * self.r - size[1]) // 2 + 3 + camera.y))

        if self.highlight:
            pygame.draw.circle(win, (255, 255, 255), (self.x + camera.x, self.y + camera.y), self.r + 2, 4)

    def move_all(self, rel):
        self.x += rel[0]
        self.y += rel[1]

        self.moved = True

        for atom in self.connections:
            if not atom.moved:
                atom.move_all(rel)


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
                    try:
                        self.list[i][j] = tuple(map(int,
                                                    self.list[i][j].split(",")))
                    except:
                        pass

        table.close()


class Popup:
    def __init__(self, w, h, color, buttons, labels):
        self.x = (WIN_SIZE[0] - w) // 2
        self.y = (WIN_SIZE[1] - h) // 2

        self.w = w
        self.h = h

        self.color = color

        self.buttons = buttons
        self.labels = labels
        self.inputs = []

        self.bg = pygame.Surface((WIN_SIZE[0], WIN_SIZE[1]))
        self.bg.fill(self.color)
        self.bg.set_alpha(200)

    def draw(self):
        win.blit(self.bg, (0, 0))

        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

        for label in self.labels:
            label.draw((self.x, self.y))

        for button in self.buttons:
            button.draw((self.x, self.y))

        for input_box in self.inputs:
            input_box.draw((self.x, self.y))

    def update_pos(self, new_w, new_h):
        self.bg = pygame.transform.scale(self.bg, (new_w, new_h))

        self.x = (new_w - self.w) // 2
        self.y = (new_h - self.h) // 2


class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.rel = [0, 0]

        self.selected = None
        self.selected_conn = None

        self.temp_conn = None

    def update_pos(self):
        pos = pygame.mouse.get_pos()

        self.x = pos[0]
        self.y = pos[1]

    def update_rel(self):
        rel = pygame.mouse.get_rel()

        self.rel = rel

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not popup:
                arr = menu

                for button in panel.buttons:
                    if button.selected:
                        button.click()

                for button in top_bar.buttons:
                    if button.selected:
                        button.click()

            else:
                arr = popup

                for ib in popup.inputs:
                    if self.x >= ib.x + popup.x and self.x < ib.x + ib.w + popup.x and self.y >= ib.y + popup.y and self.y < ib.y + ib.h + popup.y:
                        ib.selected = True

                    else:
                        ib.selected = False

            for button in arr.buttons:
                if button.selected:
                    button.click()

    def select(self):
        if not popup:
            for button in menu.buttons:
                button.selected = self.intersecting_button(button, menu)

                if button != menu.buttons[0]:
                    indx = menu.buttons.index(button) - 1

                    atoms[indx].highlight = button.selected

            for i in range(len(atoms) - 1, -1, -1):
                if self.intersecting_atom(atoms[i]):
                    self.selected = atoms[i]
                    
                    if not camera.active:
                        self.selected.highlight = True

                    break

            for conn in connections:
                if self.intersecting_conn(conn):
                    self.selected_conn = conn

                    break

                else:
                    self.selected_conn = None

            for button in panel.buttons:
                button.selected = self.intersecting_button(button, panel)

            for button in top_bar.buttons:
                button.selected = self.intersecting_button(button, top_bar)

        else:
            for button in popup.buttons:
                button.selected = self.intersecting_button(button, popup)

    def press(self):
        if self.get_pressed(0):
            if camera.active:
                camera.x += self.rel[0]
                camera.y += self.rel[1]

            else:
                if self.selected:
                    if len(self.selected.connections) == 0:
                        self.selected.x += self.rel[0]
                        self.selected.y += self.rel[1]

                    elif len(self.selected.connections) == 1:
                        angle = math.degrees(math.atan2(self.y - camera.y - self.selected.connections[0].y, self.x - camera.x - self.selected.connections[0].x))
                        angle = angle + 15 - ((angle + 15) % 30)

                        dist = math.sqrt((self.selected.x - self.selected.connections[0].x)**2 + (self.selected.y - self.selected.connections[0].y)**2)

                        new_x = math.cos(math.radians(angle)) * dist + self.selected.connections[0].x
                        new_y = math.sin(math.radians(angle)) * dist + self.selected.connections[0].y
                        
                        self.selected.x = new_x
                        self.selected.y = new_y

                    else:
                        self.selected.move_all(self.rel)
                        
                        for atom in atoms:
                            atom.moved = False

        elif self.get_pressed(2):
            if not camera.active:
                if self.selected:
                    if not self.temp_conn:
                        self.temp_conn = Connection(self.selected, Atom(self.x - camera.x, self.y - camera.y, 1, (0, 0, 0), "mouse"), 1)
                    else:
                        self.temp_conn.atom2.x = self.x - camera.x
                        self.temp_conn.atom2.y = self.y - camera.y

                        for i in range(len(atoms)):
                            if atoms[i] != self.selected and self.intersecting_atom(atoms[i]):
                                if self.selected not in atoms[i].connections:
                                    connect_atoms(atoms[i], self.selected, self.temp_conn.t)

                                    self.temp_conn = None
                                    self.selected = None

                                    break

        else:
            self.temp_conn = None
            self.selected = None

        #print(self.temp_conn)

    def scroll(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.selected_conn:
                if event.button == 4 or event.button == 5:
                    self.selected_conn.t = (self.selected_conn.t + 1) % 3 + 1

            if self.x < menu.w and self.y < WIN_SIZE[1]:
                if event.button == 5 and menu.buttons[0].y + menu.buttons[0].h > WIN_SIZE[1]:
                    for button in menu.buttons:
                        button.y -= 70

                elif event.button == 4 and menu.buttons[len(menu.buttons) - 1].y < 160:
                    for button in menu.buttons:
                        button.y += 70

    def get_pressed(self, mbutton):
        return pygame.mouse.get_pressed()[mbutton]

    def intersecting_atom(self, atom):
        dist = math.sqrt((self.x - camera.x - atom.x)**2 + (self.y - camera.y - atom.y)**2)

        if dist <= atom.r:
            return True

        else:
            return False

    def intersecting_button(self, button, offset):
        if button.x + offset.x <= self.x and button.x + button.w + offset.x > self.x:
            if button.y + offset.y <= self.y and button.y + button.h + offset.y > self.y:
                return True
            else:
                return False
        else:
            return False

    def intersecting_conn(self, conn):
        conn_angle = -math.degrees(math.atan2(conn.atom1.y - conn.atom2.y, conn.atom1.x - conn.atom2.x))
        mouse_angle = -math.degrees(math.atan2(self.y - camera.y - conn.atom1.y, self.x - camera.x - conn.atom1.x)) + 180

        if mouse_angle > 180:
            mouse_angle -= 360

        min_x = min(conn.atom1.x, conn.atom2.x)
        max_x = max(conn.atom1.x, conn.atom2.x)
        
        min_y = min(conn.atom1.y, conn.atom2.y)
        max_y = max(conn.atom1.y, conn.atom2.y)

        if (conn_angle >= 89 and conn_angle <= 91) or (conn_angle >= -91 and conn_angle <= -89):
            if self.y - camera.y >= min(conn.atom1.y, conn.atom2.y) and self.y - camera.y < max(conn.atom1.y, conn.atom2.y):
                if self.x - camera.x >= conn.atom1.x - 15 and self.x - camera.x < conn.atom1.x + 15:
                    return True

                else:
                    return False

            else:
                return False

        elif (conn_angle >= 179 or conn_angle <= -179) or (conn_angle <= 1 and conn_angle >= -1):
            if self.x - camera.x >= min(conn.atom1.x, conn.atom2.x) and self.x - camera.x < max(conn.atom1.x, conn.atom2.x):
                if self.y - camera.y >= conn.atom1.y - 15 and self.y - camera.y < conn.atom1.y + 15:
                    return True

                else:
                    return False

            else:
                return False

        else:
            if self.x - camera.x >= min_x and self.x - camera.x <= max_x and self.y - camera.y >= min_y and self.y - camera.y <= max_y:
                if mouse_angle >= conn_angle - 10 and mouse_angle <= conn_angle + 10:
                    return True
                
                else:
                    return False
            
            else:
                return False

    def delete_stuff(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
            if self.selected:
                delete_atom(self.selected)
                self.selected = None

            elif self.selected_conn:
                delete_conn(self.selected_conn)
                self.selected_conn = None


class Connection:
    def __init__(self, atom1, atom2, t):
        self.atom1 = atom1
        self.atom2 = atom2

        if t not in [1, 2, 3]:
            raise TypeError("Connection types include only 1, 2 and 3.")
        else:
            self.t = t

        self.angle = 0

    def draw_line(self, width, color):
        pygame.draw.line(win, color, 
            (self.atom1.x + camera.x, self.atom1.y + camera.y), 
            (self.atom2.x + camera.x, self.atom2.y + camera.y), 
            width)

    def draw(self):
        self.draw_line(30, (220, 220, 220))

        if self.t == 2:
            self.draw_line(10, (0, 0, 0))

        elif self.t == 3:
            self.draw_line(18, (0, 0, 0))
            self.draw_line(6, (220, 220, 220))


class Panel:
    def __init__(self, x, y, w, h, buttons, labels):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.buttons = buttons
        self.labels = labels

    def draw(self):
        pygame.draw.rect(win, (200, 200, 200), (self.x, self.y, self.w, self.h))

        for button in self.buttons:
            button.draw((self.x, self.y))

        for label in self.labels:
            label.draw((self.x, self.y))

    def resize(self):
        self.x = menu.w
        self.y = WIN_SIZE[1] - 40

        self.w = WIN_SIZE[0] - menu.w
        self.h = 40

        self.buttons[0].x = self.w - 40


class IconButton:
    def __init__(self, x, y, w, h, 
                 bg, icon, func, arg=None):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.bg = bg
        self.icon = icon

        self.func = func
        self.arg = arg

        self.selected = False

    def draw(self, offset):
        if self.selected:
            color = (self.bg[0] + 15,
                     self.bg[1] + 15,
                     self.bg[2] + 15)
        else:
            color = self.bg

        pygame.draw.rect(win, color, 
                         (self.x + offset[0], self.y + offset[1], 
                         self.w, self.h))

        win.blit(self.icon, (self.x + offset[0], self.y + offset[1]))

    def click(self):
        if self.arg:
            self.func(self.arg)

        else:
            self.func()


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.active = False


class InputBox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.text = ""
        self.selected = False
        self.color = (180, 180, 180)

    def draw(self, offset):
        if self.selected:
            color = (self.color[0] + 15,
                self.color[1] + 15,
                self.color[2] + 15)
        else:
            color = self.color

        pygame.draw.rect(win, color, (self.x + offset[0], self.y + offset[1], self.w, self.h))

        if normal.size(self.text)[0] + 3 > self.w:
            write_text(self.text[len(self.text) - (self.w // round(normal.size(self.text)[0] / len(self.text))) + 1 : len(self.text)], normal, (0, 0, 0), 
                (self.x + 3 + offset[0], self.y + 7 + offset[1]))

        else:
            write_text(self.text, normal, (0, 0, 0), 
                (self.x + 3 + offset[0], self.y + 7 + offset[1]))

    def update_text(self, event):
        if event.type == pygame.KEYDOWN and self.selected:
            self.text += event.unicode

            if event.key == pygame.K_RETURN:
                self.selected = False

            if event.key == pygame.K_BACKSPACE and len(self.text) > 0:
                arr = list(self.text)
                arr.pop(len(self.text) - 1)
                self.text = "".join(arr)


class TopBar:
    def __init__(self, x, y, w, h, buttons, labels):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.buttons = buttons
        self.labels = labels

    def draw(self):
        pygame.draw.rect(win, (200, 200, 200), (self.x, self.y, self.w, self.h))

        for button in self.buttons:
            button.draw((self.x, self.y))

        for label in self.labels:
            label.draw((self.x, self.y))

    def resize(self):
        self.x = menu.w
        self.y = 0

        self.w = WIN_SIZE[0] - menu.w
        self.h = 40


#MAINLOOP FUNCTIONS
def update():
    global done, WIN_SIZE, win, popup

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.VIDEORESIZE:
            WIN_SIZE = (event.w, event.h)
            win = pygame.display.set_mode(WIN_SIZE, pygame.RESIZABLE)

            menu.update_height(event.h)
            menu.update_buttons_y()

            panel.resize()
            top_bar.resize()

            if popup:
                popup.update_pos(event.w, event.h)

        mouse.delete_stuff(event)
        mouse.click(event)
        mouse.scroll(event)

        if popup:
            for ib in popup.inputs:
                ib.update_text(event)

    if not mouse.selected:
        mouse.select()

    mouse.press()

    mouse.update_rel()
    mouse.update_pos()

def redraw():
    win.fill((0, 0, 0))

    for conn in connections:
        conn.draw()

    if mouse.temp_conn:
        mouse.temp_conn.draw()

    for atom in atoms:
        atom.draw()

    menu.draw()
    panel.draw()
    top_bar.draw()

    if popup:
        popup.draw()
    
    pygame.display.update()


#PROGRAM FUNCTIONS
def choose_atom():
    global popup
    
    popup = Popup(900, 600, (210, 210, 210),
                  [Button(850, 10, 40, 40,
                          (180, 0, 0), (255, 255, 255),
                          "X", close_popup)],
                  
                  [Label(0, 0, 900, 120,
                         (0, 0, 0), (255, 255, 255),
                         "Выберите атом", header)])

    for elem in elements.list:
        color = list(elem[4])
        for i in range(3):
            if color[i] >= 70:
                color[i] -= 70
        
        popup.buttons.append(Button(90 * elem[5][0], 48 * elem[5][1] + 120,
                                    90, 48,
                                    color, (255, 255, 255),
                                    elem[0],
                                    create_atom, (25 + elem[1],
                                                  color, elem[0], elem[6]),
                                    True))

def close_popup():
    global popup
    popup = None

def create_atom(arg):
    atoms.append(Atom(WIN_SIZE[0] // 2 - camera.x, WIN_SIZE[1] // 2 - camera.y,
                      arg[0], arg[1], arg[2]))

    menu.buttons.append(Button(10, 0, 380, 60,
                               (240, 240, 240), (0, 0, 0),
                               str(arg[2] + "(" + arg[3] + ")"),
                               atom_options, atoms[len(atoms) - 1]))

    menu.update_buttons_y()

    close_popup()

def atom_options(atom):
    global popup

    popup = Popup(700, 400, (210, 210, 210),
                  [Button(650, 10, 40, 40,
                          (180, 0, 0), (255, 255, 255),
                          "X", close_popup),

                   Button(490, 350, 200, 40,
                          (240, 240, 240), (0, 0, 0),
                          "Удалить атом", delete_atom, atom)],
                  
                  [Label(0, 0, 700, 100,
                         (0, 0, 0), (255, 255, 255),
                         "Параметры атома", header),

                   Label(40, 110, 150, 40,
                         (210, 210, 210), (0, 0, 0),
                         "Название: ", normal),

                   Label(12, 150, 300, 40,
                         (210, 210, 210), (0, 0, 0),
                         "Количество связей: ", normal),

                   Label(190, 110, 50, 40,
                         (210, 210, 210), (0, 0, 0),
                         atom.name, normal),

                   Label(285, 150, 30, 40,
                         (210, 210, 210), (0, 0, 0),
                         str(len(atom.connections)), normal)])

def delete_atom(atom):
    for i in atoms:
        if i != atom and atom in i.connections:
            i.connections.pop(i.connections.index(atom))

    for i in range(len(connections)):
        if connections[i].atom1 == atom or connections[i].atom2 == atom:
            connections[i] = None

    while None in connections:
        connections.pop(connections.index(None))

    menu.buttons.pop(atoms.index(atom) + 1)
    atoms.pop(atoms.index(atom))

    menu.update_buttons_y()

    close_popup()

def connect_atoms(atom1, atom2, n):
    angle = math.degrees(math.atan2(atom1.y - atom2.y, atom1.x - atom2.x))
    angle = angle + 15 - ((angle + 15) % 30)

    new_x = math.cos(math.radians(angle)) * (atom1.r + atom2.r + 80) + atom2.x
    new_y = math.sin(math.radians(angle)) * (atom1.r + atom2.r + 80) + atom2.y

    if len(atom1.connections) == 0:
        atom1.x = new_x
        atom1.y = new_y

    else:
        atom1.move_all((new_x - atom1.x, new_y - atom1.y))

        for atom in atoms:
            atom.moved = False

    connections.append(Connection(atom1, atom2, n))

    atom1.connections.append(atom2)
    atom2.connections.append(atom1)

def clear():
    global connections, atoms

    connections = []
    atoms = []

    menu.buttons = [menu.buttons[0]]
    mouse.selected = None
    menu.update_buttons_y()

    camera.x = 0
    camera.y = 0
    camera.active = False

    panel.labels[0].text = "Рука: ВЫКЛ"
    panel.labels[0].w = 120

    close_popup()

def clear_warning():
    global popup

    popup = Popup(400, 200, (210, 210, 210), 

        [Button(70, 140, 80, 40, 
            (240, 240, 240), (0, 0, 0),
            "Да", clear),

        Button(250, 140, 80, 40,
            (240, 240, 240), (0, 0, 0),
            "Нет", close_popup)],

        [Label(0, 0, 400, 80, 
            (0, 0, 0), (255, 255, 255),
            "Вы уверены, что хотите удалить всё?", normal)])

def delete_conn(conn):
    conn.atom1.connections.pop(conn.atom1.connections.index(conn.atom2))
    conn.atom2.connections.pop(conn.atom2.connections.index(conn.atom1))

    connections.pop(connections.index(conn))

def switch_hand():
    camera.active = bool((int(camera.active) + 1) % 2)

    if camera.active:
        panel.labels[0].text = "Рука: ВКЛ"
        panel.labels[0].w = 103
    else:
        panel.labels[0].text = "Рука: ВЫКЛ"
        panel.labels[0].w = 120

def save():
    global popup

    try:
        file = open("saves/" + popup.inputs[0].text + ".txt", "w")

        for atom in atoms:
            file.write("Atom " + str(atom.x) + " " + str(atom.y) + " " + str(atom.r) + " " + str(atom.color[0]) + "," + str(atom.color[1]) + "," + str(atom.color[2]) + " " + atom.name + " " + menu.buttons[atoms.index(atom) + 1].text.split("(")[1].split(")")[0] + "\n")

        file.write("\n")

        for conn in connections:
            file.write("Connection " + str(atoms.index(conn.atom1)) + " " + str(atoms.index(conn.atom2)) + " " + str(conn.t) + "\n")

        file.close()

        close_popup()

        popup = Popup(300, 200, (210, 210, 210),
            [Button(120, 130, 60, 40, 
                (240, 240, 240), (0, 0, 0),
                "OK", close_popup)],

            [Label(0, 0, 300, 70, 
                (0, 0, 0), (255, 255, 255),
                "Файл успешно сохранен!", normal)])
    except:
        popup = Popup(300, 200, (210, 210, 210),
            [Button(120, 130, 60, 40,
                (240, 240, 240), (0, 0, 0),
                "OK", close_popup)],

            [Label(0, 0, 300, 30,
                (0, 0, 0), (255, 255, 255),
                "Имя не должно содержать", normal),

            Label(0, 30, 300, 30,
                (0, 0, 0), (255, 255, 255),
                "специальных символов!", normal)])

def load(mode):
    global popup

    try:

        file = open("saves/" + popup.inputs[0].text + ".txt", "r")

        arr = file.read()

        arr = arr.split("\n\n")
        for i in range(len(arr)):
            arr[i] = arr[i].split("\n")
            for j in range(len(arr[i])):
                arr[i][j] = arr[i][j].split()
                for g in range(len(arr[i][j])):
                    try:
                        arr[i][j][g] = int(arr[i][j][g])
                    except:
                        try:
                            arr[i][j][g] = tuple(map(int, arr[i][j][g].split(",")))
                        except:
                            try:
                                arr[i][j][g] = float(arr[i][j][g])
                            except:
                                pass

        file.close()

        if mode == "load":
            clear()
            k = 0
        else:
            k = len(atoms)

        for atom in arr[0]:
            atoms.append(Atom(atom[1], atom[2], atom[3], atom[4], atom[5]))
            
            menu.buttons.append(Button(10, 0, 380, 60, 
                (240, 240, 240), (0, 0, 0),
                atom[5] + "(" + atom[6] + ")", atom_options,
                atoms[len(atoms) - 1]))

        arr[1].pop(len(arr[1]) - 1)
        menu.update_buttons_y()

        for conn in arr[1]:
            connect_atoms(atoms[conn[1] + k], atoms[conn[2] + k], conn[3])

        popup = Popup(300, 200, (210, 210, 210),
            [Button(120, 130, 60, 40, 
                (240, 240, 240), (0, 0, 0),
                "OK", close_popup)],

            [Label(0, 0, 300, 70, 
                (0, 0, 0), (255, 255, 255),
                "Файл успешно загружен!", normal)])
    except:
        popup = Popup(300, 200, (210, 210, 210),
            [Button(120, 130, 60, 40,
                (240, 240, 240), (0, 0, 0),
                "OK", close_popup)],

            [Label(0, 0, 300, 60,
                (0, 0, 0), (255, 255, 255),
                "Файл не найден!", normal)])

def save_options():
    global popup

    popup = Popup(400, 300, (210, 210, 210),
        [Button(350, 10, 40, 40,
            (180, 0, 0), (255, 255, 255),
            "X", close_popup),
        
        Button(140, 260, 120, 30,
            (240, 240, 240), (0, 0, 0),
            "Сохранить", save)],

        [Label(0, 0, 400, 100, 
            (0, 0, 0), (255, 255, 255),
            "Сохранение", header),

        Label(0, 110, 100, 40,
            (210, 210, 210), (0, 0, 0),
            "Имя: ", normal)])

    popup.inputs.append(InputBox(100, 110, 200, 40))

def load_options(mode):
    global popup

    popup = Popup(400, 300, (210, 210, 210),
        [Button(350, 10, 40, 40,
            (180, 0, 0), (255, 255, 255),
            "X", close_popup),

        Button(140, 260, 120, 30, 
            (240, 240, 240), (0, 0, 0),
            "Загрузить", load, mode)],

        [Label(0, 0, 400, 100,
            (0, 0, 0), (255, 255, 255),
            "Загрузка", header),

        Label(0, 110, 100, 40, 
            (210, 210, 210), (0, 0, 0),
            "Имя: ", normal)])

    popup.inputs.append(InputBox(100, 110, 200, 40))

def import_options(mode):
    global popup

    popup = Popup(400, 300, (210, 210, 210),
        [Button(350, 10, 40, 40,
            (180, 0, 0), (255, 255, 255),
            "X", close_popup),

        Button(115, 260, 170, 30, 
            (240, 240, 240), (0, 0, 0),
            "Импортировать", load, mode)],

        [Label(0, 0, 400, 100,
            (0, 0, 0), (255, 255, 255),
            "Импорт", header),

        Label(0, 110, 100, 40, 
            (210, 210, 210), (0, 0, 0),
            "Имя: ", normal)])

    popup.inputs.append(InputBox(100, 110, 200, 40))


#CONVENIENCE FUNCTIONS
def write_text(text, font, color, coords):
    img = font.render(text, True, color)
    win.blit(img, coords)


#VARIABLES
elements = ElementsList("elements.txt")
elements.openFile()

popup = None

menu = Menu(400, (220, 220, 220),
            
            [Button(10, 160, 380, 60,
                    (240, 240, 240), (0, 0, 0),
                    "+ Создать атом", choose_atom)],
            
            [Label(0, 0, 400, 150,
                   (255, 255, 255), (0, 0, 0),
                   "Список атомов", header)])

panel = Panel(menu.w, WIN_SIZE[1] - 40, WIN_SIZE[0] - menu.w, 40, 

    [IconButton(WIN_SIZE[0] - 40 - menu.w, 5, 30, 30, 
                (240, 240, 240), 
                pygame.image.load("icons/bin.png").convert_alpha(),
                clear_warning),

    IconButton(5, 5, 30, 30,
        (240, 240, 240),
        pygame.image.load("icons/hand.png").convert_alpha(),
        switch_hand)], 

    [Label(40, 5, 120, 30, 
        (200, 200, 200), (0, 0, 0),
        "Рука: ВЫКЛ", normal)])

top_bar = TopBar(menu.w, 0, WIN_SIZE[0] - menu.w, 40,
    [Button(5, 5, 120, 30, 
        (240, 240, 240), (0, 0, 0),
        "Сохранить", save_options),

    Button(130, 5, 120, 30,
        (240, 240, 240), (0, 0, 0),
        "Загрузить", load_options, "load"),

    Button(255, 5, 170, 30, 
        (240, 240, 240), (0, 0, 0),
        "Импортировать", import_options, "import")], [])

atoms = []
connections = []

mouse = Mouse()
camera = Camera()

#MAINLOOP
done = False
while not done:
    update()

    redraw()

pygame.quit()
