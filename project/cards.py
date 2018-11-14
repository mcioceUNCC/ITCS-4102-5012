import glob
import pygame as pg
import random

# Returns a dict of all cards
# Cards are keyed as a number 2-10 or J/Q/K/A for value, then C/D/H/S for suit
# So Ace of Spades would be AS
# 7 of Hearts would be 7H
def loadCardImages():
	deckImages = {}
	baseDir = "card_images/"
	# Get all card faces
	for path in glob.iglob(baseDir + "[0-9JQKA]*[CDHS].png"):
		deckImages[path[len(baseDir):-4]] = pg.image.load(path)
	# Load in the card back as well
	deckImages["back"] = pg.image.load(baseDir + "back_grey.png")
	return deckImages

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

# Run the file directly to use this for testing
if __name__ == '__main__':
	print(generateDeckArray())