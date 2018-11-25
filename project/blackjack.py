import pygame as pg
import cards

pg.init()
pg.font.init()

display = pg.display.set_mode((1280, 720))
defaultFont = pg.font.Font(None, 26)

DEFAULT_CARD_SIZE = (100, 153)

# Load in face/back images
cardImages = cards.loadCardImages(DEFAULT_CARD_SIZE)

dealerDeck = cards.shuffle(cards.generateDeckArray())
dealerHand = []
dealerHandElements = []
playerHand = []
playerHandElements = []

buttonElements = []


def main():
	ButtonElement(position = (1170, 10), text = "Hit", clickAction = hit)
	ButtonElement(position = (1170, 70), text = "Stand", clickAction = lambda: print("Stand button clicked"))
	ButtonElement(position = (1170, 130), text = "Deal", clickAction = lambda: print("Deal button clicked"))

	newHand()

	exit = False
	# Keep going until the player exits or there are no more cards in the deck
	while len(dealerDeck) != 0:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return # Player exited the window

			if event.type == pg.MOUSEBUTTONUP:
				print(pg.mouse.get_pos())
				for button in buttonElements:
					if button.mouseInElement():
						button.click()
		display.fill((60,180,45))

		for button in buttonElements:
			button.draw()

		for card in (dealerHandElements + playerHandElements):
			card.draw()

		if handValue(playerHand) > 21:
			display.blit(*newTextObject(pg.font.Font(None, 36),
				                        "You went bust! Click \"Deal\" to start a new round.",
				                        (640, 360)))
			pg.display.flip()
			continue

		# Add other logic here

		pg.display.flip()


def handValue(hand):
	total = 0;
	for card in hand:
		total += cards.value(card)

	return total

# Deals the player a new card
def hit():
	playerHand.append(*cards.draw(dealerDeck, 1))
	playerHandElements.append(*genCardElements([playerHand[-1]], 
		                      startPos = (playerHandElements[-1].position[0]+DEFAULT_CARD_SIZE[0]+ 10, 
		                      	          720-DEFAULT_CARD_SIZE[1]-10)))

def newHand():
	global dealerHand, dealerHandElements
	global playerHand, playerHandElements
	dealerHand = cards.draw(dealerDeck, 2)
	
	dealerHandElements = genCardElements(dealerHand, startPos = (10, 10))
	dealerHandElements[0].flip()
	playerHand = cards.draw(dealerDeck, 2)
	playerHandElements = genCardElements(playerHand, startPos = (10, 720-DEFAULT_CARD_SIZE[1]-10))


class Element():
	def __init__(self, position = (0, 0), size = (0, 0)):
		self.position = position
		self.size = size


	def draw(self):
		pass


	# Returns whether the mouse is currently inside the button area or not
	def mouseInElement(self):
		mouseLoc = pg.mouse.get_pos()
		return self.position[0] < mouseLoc[0] < self.position[0]+self.size[0] and \
		       self.position[1] < mouseLoc[1] < self.position[1]+self.size[1]


# A rectangular button with text on it
class ButtonElement(Element):
	def __init__(self, position = (0, 0), size = (100, 50), color = (255, 255, 255), text = "", textColor = (0, 0, 0), clickAction = lambda: None):
		super().__init__(position = position, size = size)
		self.color = color
		self.text = text
		self.textColor = textColor
		self.click = clickAction
		buttonElements.append(self)


	def draw(self):
		drawColor = self.color
		if self.mouseInElement():
			# Draw the button slightly differently since it's being hovered over
			# Be careful not to make the buttons too dark if you use a black font, since it could hide the text
			drawColor = tuple(abs(a-20) for a in self.color)

		# * is for unpacking the tuples
		pg.draw.rect(display, drawColor, (*self.position, *self.size))
		textSurf, textRect = newTextObject(defaultFont, self.text, 
			                               (self.position[0]+(self.size[0]/2), self.position[1]+(self.size[1]/2)),
			                               color = self.textColor)
		display.blit(textSurf, textRect)


# A single image of a card. Use "back" card ID to draw the back of a card, or set "shown" to False
class CardElement(Element):
	def __init__(self, position = (0, 0), size = DEFAULT_CARD_SIZE, cardId = "AS", shown = True, clickAction = lambda: None):
		super().__init__(position = position, size = size)
		self.cardId = cardId
		self.click = clickAction
		self.shown = shown


	def draw(self):
		display.blit(cardImages[self.cardId if self.shown else "back"], self.position)


	def flip(self):
		self.shown = not self.shown


def newTextObject(font, text, center, color = (0, 0, 0)):
	rendered = font.render(text, True, color)
	return rendered, rendered.get_rect(center=center)

# Returns an array of CardElements that are layed out horizontaly
def genCardElements(cardIds, startPos = (0, 0)):
	cardElements = []
	for i, cardId in zip(range(0, len(cardIds)), cardIds):
		cardElements.append(CardElement(position = ((DEFAULT_CARD_SIZE[0]+10)*i+startPos[0], startPos[1]), cardId = cardId))

	return cardElements


if __name__ == "__main__":
	main()
