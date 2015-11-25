from collections import Counter
from itertools import permutations
from functools import partial
from re import findall

alphabet = list(map(chr, range(97, 123)))
KONSTANT = 5

# A cipher is a mapping from the alphabet in an encoded space to the alphabet in english.
# It is initalized with whatever part of that mapping is known or suspected and a score function
class Cipher:
	# We store the essence of a cipher in two ways: a list of tuples and a dict.
	# The cipher is scored at initialization.
	# A cipher should be thought of as immutable. To "change" the cipher, create a new Cipher
	# with the old cipher's mapping concatenated with the new mapping.
	def __init__(self, mapping, scoreFunction):
		self.cipher = {c: None for c in alphabet}
		self.mapping = mapping
		self.cipher.update(dict(mapping))
		self.score = scoreFunction(self)

	# We represent ciphers by their mappings
	def __repr__(self):
		return '\n'.join([encoded+' -> '+str(decoded) for encoded, decoded in self.cipher.items()])

	# We sort ciphers by their scores.
	def __gt__(self, other):
		return self.score > other.score

	# Replace each letter in the sample with its cipher unless it's punctuation, space, etc...
	# If we don't know what the letter ciphers to, uppercase the unciphered letter.
	def decipher(self, sample):
		return ''.join([self.cipher[c] if c in self.cipher and self.cipher[c] != None else c.upper() for c in sample])

	# Return the *single* most popular character from the domain of the cipher which is unmapped:
	# the most popular character in the encoded string which we don't have a translation for.
	def mostPopularUnmappedCharacter(self, sampleCharacters):
		for c in list(zip(*sampleCharacters.most_common())[0]):
			if self.cipher[c] == None: return [c]
		return []

	# Return the *KONSTANT* most popular characters in the corpus which do not yet exist in the codomain of the cipher.
	def mostPopularUnassignedCharacters(self, corpusCharacters):
		return [c for c in list(zip(*corpusCharacters.most_common())[0]) if c not in filter(None, self.cipher.values())][:KONSTANT]


########################## Main Program ##########################


def main():

	languageModel, characterModel = analyze("corpus-en.txt")

	encoded, words, characters = extract("encoded-en.txt")

	cipher = decode(encoded, words, characters, languageModel, characterModel)

	print cipher
	print cipher.decipher(encoded)

# Read a corpus out of a file and return a dict of frequencies
# for each character and each word in the corpus.
def analyze(corpus):

	languageModel = Counter()
	characterModel = Counter()

	with open(corpus, "r") as f:
		for line in f:
			words = findall(r"[a-z]+", line.lower())
			languageModel.update(words)

	for word, freq in languageModel.items():
		characterModel.update({c: freq for c in word})

	return languageModel, characterModel

# Read a sample of text from a file and return the string,
# a list of each word in the string, and a dict of frequencies
# of each letter in the alphabet in the sample.
def extract(sample):

	string = open(sample, "r").read().lower()
	sampleWords = findall(r"[a-z]+", string)
	sampleCharacters = Counter(''.join(sampleWords))

	return string, sampleWords, sampleCharacters

# This is the principal algorithm responsible for decoding the encoded string, and determining the cipher.
def decode(encoded, words, characters, languageModel, characterModel):

	# First, take the KONSTANT most-common single-letter words from the corpus (turns out to be all 26 letters),
	# and all the single letter words from the encoded string (there are only two of these).
	singleLetterCorpusWords = set([word for word, count in filterByWordLength(languageModel, 1).most_common(KONSTANT)])
	singleLetterSampleWords = set([word for word in words if len(word) == 1])

	scoreFn = partial(cipherScore, languageModel, characterModel, words, characters)

	# Generate every possible assignment from the sample single-letter words to the corpus single-letter words.
	# Then initialize a Cipher object for each of them with that assignment as its seed. Put them in a pool
	pool = [Cipher(seed, scoreFn) for seed in everyPossibleAssignment(singleLetterSampleWords, singleLetterCorpusWords)]

	iteration = 0

	# Loop until the best cipher in the pool has an idea for what each character in the sample maps to.
	while pool[0].mostPopularUnmappedCharacter(characters) != []:

		newpool = []

		# For each cipher in the pool, select the next most popular character from the sample
		# and the  next KONSTANT most popular characters from the corpus to create a set of possible assignments
		for cipher in pool:

			assignments = everyPossibleAssignment(cipher.mostPopularUnmappedCharacter(characters),
												  cipher.mostPopularUnassignedCharacters(characterModel))

			# Create a new cipher for each of these possible augmentations of the old cipher.
			newpool += [Cipher(cipher.mapping + assignment, scoreFn) for assignment in assignments]

		pool = newpool

		if iteration > 1:

			# Sort the ciphers by fitness and throw away the worst ones.
			pool.sort(reverse=True)
			del pool[(len(pool) / KONSTANT):]

		iteration += 1

	return pool[0]

# Take a slice of a Counter, keeping only the keys of len(key) == length. Returns a Counter.
def filterByWordLength(languageModel, length):

	return Counter({word: freq for word, freq in languageModel.items() if len(word) == length})

# Produce every one-to-one mapping from elements of A to elements of B. |A| must be smaller than |B|.
def everyPossibleAssignment(A, B):

	if len(A) < len(B): return [list(zip(A, P)) for P in permutations(B, len(A))]
	else: print "Violation of terms: len(A) must be less than len(B)"

# languageModel stores counts of words in the corpus. We score a cipher by how many words it forms
# in the encoded string, with the score of each word being its number of occurrences in the corpus.
def wordCompletionScore(languageModel, cipher, encodedWords):

	return sum([languageModel[cipher.decipher(word)] for word in encodedWords])

# This function merely wraps wordCompletionScore now, but was initially intially intended to take
# the difference between two metrics of fitness. Read below for more.
def cipherScore(languageModel, characterModel, words, characters, cipher):

	return wordCompletionScore(languageModel, cipher, words) # - cipherDisalignment(characterModel, cipher.cipher, characters)



if __name__ == '__main__': main()


########################## Graveyard of Old Code ##########################


# The initial plan was to have cipherDisalignment be a term in the score function, which would
# represent the disalignment between the frequencies of the characters in the corpus and the string
# decoded with a given cipher, using ChiSquared statistics. I eventually just threw this idea out,
# because it didn't seem necessary, and weighing cipherDisalignment vs wordCompletionScore would
# have been challenging. Doesn't look like it was necessary!
# CharacterModel is a Counter of characters -> counts in the corpus
# Cipher is a map from characters to characters or None
# CharacterCounts is a Counter of characters -> counts in the encoded string
def cipherDisalignment(characterModel, cipher, characterCounts):

	sampleCharacterSize = sum(characterCounts.values())

	expectedDistribution = normalize(characterModel)
	expectedCounts = {c: (sampleCharacterSize * p) for c, p in expectedDistribution.items()}

	observedCounts = {cipher[c]: i for c, i in characterCounts.items() if c in cipher and cipher[c] != None}

	return chiSquareStat(observedCounts, expectedCounts)


# Since the DOF is always 25, and since integration is expensive, we'll just compare ChiSquare
# Statistics, where anything inside the neighborhood of 20 is probably okay, and above that, we're
# heavily deviating from our expected distribution.
def chiSquareStat(observed, expected):

	return sum([(observed[c] - expected[c])**2 / float(expected[c]) for c in observed.keys()])


# Turn a counter into a maximum likelihood probability distribution
def normalize(counter):

	total = float(sum(counter.values()))
	return {item: freq/total for item, freq in counter.items()}
