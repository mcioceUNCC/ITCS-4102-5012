import pygame as pg
import cards
import sys

pg.init()
pg.font.init()

display = pg.display.set_mode((1280, 720))
defaultFont = pg.font.Font(None, 26)

DEFAULT_CARD_SIZE = (100, 153)

# Load in face/back images
cardImages = cards.loadCardImages(DEFAULT_CARD_SIZE)

dealerDeck = []
dealerHand = []
dealerHandElements = []
playerHand = []
playerHandElements = []

buttonElements = []

stayed = False

def main():
	ButtonElement(position = (1170, 10), text = "Hit", clickAction = lambda: hit(playerHand, playerHandElements))
	ButtonElement(position = (1170, 70), text = "Stand", clickAction = stand)
	ButtonElement(position = (1170, 130), text = "Deal", clickAction = newHand)

	while True:
		pg.time.delay(500)
		newGame()
		display.fill((60,180,45))
		display.blit(*newTextObject(pg.font.Font(None, 36),
		                            "Deck is being reshuffled...",
		                            (640, 360)))
		pg.display.flip()
		pg.time.delay(500)


def newGame():
	global dealerDeck, stayed

	dealerDeck = cards.shuffle(cards.generateDeckArray())
	newHand()

	roundOver = False
	stayed = False
	exit = False

	# Keep going until the player exits or there are not enough cards in the deck
	while len(dealerDeck) > 6:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sys.exit() # Player exited the window

			if event.type == pg.MOUSEBUTTONUP:
				# If the round has ended, only let the player click on the deal button
				if roundOver:
					if buttonElements[2].mouseInElement():
						roundOver = False
						stayed = False

						buttonElements[2].click()
				else:
					for button in buttonElements:
						if button.mouseInElement():
							button.click()

		# Write the green backdrop
		display.fill((60,180,45))

		# Cycle through all elements and draw them
		for element in buttonElements + dealerHandElements + playerHandElements:
			element.draw()

		# Player busted
		if handValue(playerHand) > 21:
			announcement("You went bust! Click \"Deal\" to start a new round.")
			roundOver = True

		# Player got a blackjack
		if handValue(playerHand) == 21:
			# Dealer also got a blackjack, causing a tie
			if handValue(dealerHand) == 21:
				# Only flip the card over if they tied
				if not roundOver:
					dealerHandElements[0].flip()
				announcement("You tied with the dealer. Click \"Deal\" to start a new round.")
			else:
				announcement("You got a blackjack! Click \"Deal\" to start a new round.")

			roundOver = True

		if stayed:
			# Since the player stayed, we always flip the card
			if not roundOver:
				dealerHandElements[0].flip()

			# After staying, player has a better hand than the dealer
			if handValue(playerHand) > handValue(dealerHand):
				announcement("You won! Click \"Deal\" to start a new round.")

			# After staying, player has a worse hand than the dealer
			if handValue(playerHand) < handValue(dealerHand):
				# ...However the dealer busted
				if handValue(dealerHand) > 21:
					announcement("Dealer busted. You win!. Click \"Deal\" to start a new round.")
				else:
					announcement("You lost. Click \"Deal\" to start a new round.")

			# After staying, player has an equivalent
			if handValue(playerHand) == handValue(dealerHand):
				announcement("You tied. Click \"Deal\" to start a new round.")

			roundOver = True

		# Add other logic here

		pg.display.flip()

# Sums up the hand value, automatically selecting a good value for aces
def handValue(hand):
	total = 0;
	for card in hand:
		total += cards.value(card)

	# If the hand would cause a bust, check for aces and, if they're present, which them to their low value until the hand no longer busts
	if total > 21:
		for card in hand:
			if card[0] == "A":
				total -= 10
				if total <= 21:
					break

	return total


def stand():
	global stayed
	stayed = True
	while handValue(dealerHand) < 17:
		pg.time.delay(250)
		hit(dealerHand, dealerHandElements)


# Deals a new card to the hand
def hit(hand, elements):
	hand.append(*cards.draw(dealerDeck, 1))
	elements.append(*genCardElements([hand[-1]], startPos = (elements[-1].position[0]+DEFAULT_CARD_SIZE[0] + 10,
		                                                     elements[-1].position[1])))


# Deal out 2 cards to the player and the dealer, with one of the dealers cards face down
def newHand():
	global dealerHand, dealerHandElements
	global playerHand, playerHandElements
	dealerHand = cards.draw(dealerDeck, 2)

	dealerHandElements = genCardElements(dealerHand, startPos = (10, 10))
	dealerHandElements[0].flip()
	playerHand = cards.draw(dealerDeck, 2)
	playerHandElements = genCardElements(playerHand, startPos = (10, 720-DEFAULT_CARD_SIZE[1]-10))


# Anything that can be drawn is an element
class Element():
	def __init__(self, position = (0, 0), size = (0, 0)):
		self.position = position
		self.size = size


	def draw(self):
		pass


	# Returns whether the mouse is currently inside the element area or not
	def mouseInElement(self):
		mouseLoc = pg.mouse.get_pos()
		return self.position[0] < mouseLoc[0] < self.position[0]+self.size[0] and \
		       self.position[1] < mouseLoc[1] < self.position[1]+self.size[1]


# A rectangular button with text on it
class ButtonElement(Element):
	def __init__(self, position = (0, 0), size = (100, 50),
		         color = (255, 255, 255), text = "",
		         textColor = (0, 0, 0), clickAction = lambda: None):
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
	def __init__(self, position = (0, 0),
		         size = DEFAULT_CARD_SIZE, cardId = "AS",
		         shown = True, clickAction = lambda: None):
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

# Used this exact format a lot, so just streamline it
def announcement(text):
	display.blit(*newTextObject(pg.font.Font(None, 36), text, (640, 360)))

# Returns an array of CardElements that are layed out horizontaly
def genCardElements(cardIds, startPos = (0, 0)):
	cardElements = []
	for i, cardId in zip(range(0, len(cardIds)), cardIds):
		cardElements.append(CardElement(position = ((DEFAULT_CARD_SIZE[0]+10)*i+startPos[0], startPos[1]), cardId = cardId))

	return cardElements


if __name__ == "__main__":
	main()
