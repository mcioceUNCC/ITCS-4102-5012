import glob
import pygame as pg
import random

# Returns a dict of all cards
# Cards are keyed as a number 2-10 or J/Q/K/A for value, then C/D/H/S for suit
# So Ace of Spades would be AS
# 7 of Hearts would be 7H
# Size is the (x, y) pixel size
def loadCardImages(size = (691, 1056)):
	deckImages = {}
	baseDir = "card_images/"
	# Get all card faces
	for path in glob.iglob(baseDir + "[0-9JQKA]*[CDHS].png"):
		deckImages[path[len(baseDir):-4]] = pg.transform.smoothscale(pg.image.load(path), size)
	# Load in the card back as well
	deckImages["back"] = pg.transform.smoothscale(pg.image.load(baseDir + "back_grey.png"), size)
	return deckImages

# This is if you want a single new card image of a different size for whatever reason
# If you want a back image, you must postpend it with the color to match the filename.
# choices are: blue, green, grey, purple, red, and yellow
def loadCardImage(cardId, size = (691, 1056)):
	return pg.transform.smoothscale(pg.image.load("card_images/" + cardId + ".png"), size)

# Returns an array of 52 strings for each card
# Order is not guaranteed
def generateDeckArray():
	deck = []
	baseDir = "card_images/"
	for path in glob.iglob(baseDir + "[0-9JQKA]*[CDHS].png"):
		deck.append(path[len(baseDir):-4])
	return deck

# Just a quick function for getting a new shuffled array
def shuffle(deck):
	shuffledDeck = random.sample(deck, len(deck))
	return shuffledDeck

# Returns some number of cards from the deck while also removing them
def draw(deck, numCards):
	drawnCards = []
	for i in range(0, numCards):
		drawnCards.append(deck.pop())
	return drawnCards

# Returns the numarical value for a card
def value(cardId):
	# 2-10 are just the face value
	if cardId[:-1].isdigit():
		return int(cardId[:-1])

	# All royal cards are worth 10
	return 10 if cardId[0] in ["J", "Q", "K"] else 11


# Run the file directly to use this for testing
if __name__ == '__main__':
	values = []
	cards = generateDeckArray()
	for card in cards:
		values.append(value(card))
	print(values, cards)
