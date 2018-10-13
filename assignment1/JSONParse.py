import re
import pprint
from sys import argv

def syntaxCheck(jsonString):
	if jsonString[0] != '{' or jsonString[-1] != '}':
		return False
	return bracketsMatch(jsonString)

# check if all open brackets/braces have a corresponding close character
def bracketsMatch(string):
	bracketStack = []
	braceStack = []
	balanced = True
	i = 0
	while i<len(string) and balanced:
		char = string[i]
		if char == "[":
			bracketStack.append(char)
		elif char == "{":
			braceStack.append(char)
		elif char == "]":
			if len(bracketStack) == 0:
				print("Bad \"]\" at char " + str(i))
			else:
				bracketStack.pop()
		elif char == "}":
			if len(braceStack) == 0:
				print("Bad \"}\" at char " + str(i))
			else:
				braceStack.pop()
		i+=1
	err = ""

	if len(bracketStack) != 0:
		err += str(len(bracketStack)) + " extra brackets found.\n"
	if len(braceStack) != 0:
		err += str(len(braceStack)) + " extra braces found.\n"

	if err != "":
		print(err)

	return balanced and err == ""

def tokenize(string):
	return list(filter(None, re.split(r"([\{\}\[\]\",:])", string))) # Split on any viable token, then remove empty strings from list

# Reconnects string tokens that were split during tokanization
def fixEscapedStrings(tokens):
	tokensIter = iter(tokens)
	newTokens = []
	
	while True:
		try:
			token = next(tokensIter)
		except StopIteration:
			return newTokens

		if token not in ["\"", "'"]:
			newTokens.append(token)
			continue

		stringToken = ""
		quoteType = token
		lastChar = token[-1]
		while True:
			try:
				token = next(tokensIter)
			except StopIteration:
				print("Unmatched quote found. Exiting.")
				quit()

			if token != quoteType:
				lastChar = token[-1]
				stringToken += token
				continue

			if lastChar == "\\":
				lastChar = token[-1]
				stringToken += token
				continue

			newTokens.append(stringToken)

			break

def parseObject(tokensIter):
	token = None
	jsonDict = {}

	key = ""
	haveKey = False
	
	while True:
		try:
			lastToken = token
			token = next(tokensIter)
		except StopIteration:
			return jsonDict
		
		if token == "}":
			return jsonDict

		if token == ":":
			key = lastToken
			haveKey = True

		if haveKey:
			jsonDict[key] = parseValue(tokensIter)
			haveKey = False;


def parseArray(tokensIter):
	jsonList = []
	lastToken = ","
	while True:
		if lastToken == ",":
			jsonList.append(parseValue(tokensIter))
		try:
			token = next(tokensIter)
		except StopIteration:
			return jsonList

		if token == "]":
			return jsonList


def parseValue(tokensIter):
	while True:
		try:
			token = next(tokensIter)
		except StopIteration:
			print("Something went wrong in value parsing: " + str(list(tokensIter)))
			quit()

		# Null
		if token == "null":
			return None

		# Boolean
		if token in ["true", "false"]:
			return token == "true"

		# Array
		if token == "[":
			return parseArray(tokensIter)

		# Object
		if token == "{":
			return parseObject(tokensIter)

		# Number
		if isInt(token):
			return int(token)
		elif isFloat(token):
			return float(token)

		# String
		return token


def isInt(string):
	try: 
		int(string)
		return True
	except ValueError:
		return False


def isFloat(string):
	try:
		float(string)
		return True
	except ValueError:
		return False


def parseJSON(string):
	return parseValue(iter(fixEscapedStrings(tokenize(string))))


if __name__ == "__main__": # Only run code if the script is being called directly, not if it's imported
	if len(argv) > 2:
		print("Incorrect number of arguments. Pass one file to parse it, or none to parse demo YouTube API JSON response file (\"File.json\")")
		quit()
	
	inputFile = argv[1] if len(argv) == 2 else "File.json"
	
	with open(inputFile, 'r') as file:
		jsonString = re.sub(r"\s+", '', file.read()) # load the file into a string and strip whitespace
	
	pp = pprint.PrettyPrinter(indent=4) # For better dict formatting

	if syntaxCheck(jsonString):
		print("Parsed JSON:")
		pp.pprint(parseJSON(jsonString))
	else:
		print("Bad syntax in file. Exiting")