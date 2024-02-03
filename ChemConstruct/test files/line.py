import pygame
pygame.init()

WIN_SIZE = (500, 500)
win = pygame.display.set_mode(WIN_SIZE)

font = pygame.font.SysFont("arial", 24)


class Line:
	def __init__(self, p1, p2, w):
		self.p1 = p1
		self.p2 = p2

		self.w = w

	def draw(self):
		pygame.draw.line(win, (200, 200, 200), self.p1, self.p2, self.w)

		pygame.draw.line(win,(200, 0, 0), self.p1, self.p2)


class Text:
	def __init__(self, x, y, text):
		self.x = x
		self.y = y

		self.text = text

	def draw(self):
		img = font.render(self.text, 1, (255, 255, 255))
		win.blit(img, (self.x, self.y))


def redraw():
	win.fill((0, 0, 0))

	line.draw()
	txt.draw()

	pygame.display.update()

def update():
	global done

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

line = Line((50, 450), (450, 50), 40)
txt = Text(10, 10, str(False))

done = False
while not done:
	update()

	redraw()

pygame.quit()