import pygame as pg
import cards

pg.init()
pg.font.init()

display = pg.display.set_mode((1280, 720))
defaultFont = pg.font.Font(None, 26)

# Load in face/back images
cardImages = cards.loadCardImages()

dealerDeck = cards.shuffle(cards.generateDeckArray())
dealerHand = []
playerHand = []

buttons = []

# A rectangular button with text on it
class Button():
	def __init__(self, position = (0, 0), color = (255, 255, 255), size = (100, 50), text = "", clickAction = lambda: None):
		self.position = position
		self.color = color
		self.size = size
		self.text = text
		self.click = clickAction
		buttons.append(self)

	def draw(self):
		drawColor = self.color
		if self.mouseInButton():
			# Draw the button slightly differently since it's being hovered over
			# Be careful not to make the buttons too dark, since it may end up hiding the black text
			drawColor = tuple(abs(a-20) for a in self.color)

		# * is for unpacking the tuples
		pg.draw.rect(display, drawColor, (*self.position, *self.size))
		textSurf, textRect = newTextObject(defaultFont, self.text, (self.position[0]+(self.size[0]/2), self.position[1]+(self.size[1]/2)))
		display.blit(textSurf, textRect)

	# Returns whether the mouse is currently inside the button area or not
	def mouseInButton(self):
		mouseLoc = pg.mouse.get_pos()
		return self.position[0] < mouseLoc[0] < self.position[0]+self.size[0] and \
		       self.position[1] < mouseLoc[1] < self.position[1]+self.size[1]

def main():

	Button(position = (200, 200), text = "Testing", clickAction = lambda: print("Test button clicked"))

	exit = False
	# Keep going until the player exits or there are no more cards in the deck
	while len(dealerDeck) != 0:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return # Player exited the window

			if event.type == pg.MOUSEBUTTONUP:
				for button in buttons:
					if button.mouseInButton():
						button.click()

		display.fill((60,180,45))

		for button in buttons:
			button.draw()
		# Add other logic here

		pg.display.flip()

def newTextObject(font, text, center, color = (0, 0, 0)):
	rendered = font.render(text, True, color)
	return rendered, rendered.get_rect(center=center)

if __name__ == "__main__":
	main()