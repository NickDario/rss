from nltk.corpus import PlaintextCorpusReader
from nltk import word_tokenize
from nltk import pos_tag

CORPUS_DIR = '/home/nick/nltk_data/dict'

sentiment_corpus = PlaintextCorpusReader(CORPUS_DIR, [
	'positive-words.txt',
	'negative-words.txt',
])


test = raw_input()

negative = open(CORPUS_DIR + '/negative-words.txt')
negative_set = [x.strip('\n') for x in negative.readlines()]

positive = open(CORPUS_DIR + '/positive-words.txt')
positive_set = [x.strip('\n') for x in positive.readlines()]
#
#	corpus split hyphenated words
#
#positive_set = [word for word in sentiment_corpus.words('positive-words.txt')]
#negative_set = [word for word in sentiment_corpus.words('negative-words.txt')]

score = 0

tags = pos_tag(word_tokenize(test))

#
# Adverbs, Adjectives, other
# being positive or negative is dependent on the noun or verb
# that is being modified.
#
def analyzeModifier(word):
	if word in positive_set:
		return 1
	if word in negative_set:
		return -1
	return 1
	
def analyzeNoun(word):
	if word in positive_set:
		return 10
	if word in negative_set:
		return -10
	return 0

def analyzeVerb(word):
	if word in positive_set:
		return 10
	if word in negative_set:
		return -10
	return 0

def analyzeBase(word):
	if word in positive_set:
		print('+' + word)
		return 10
	if word in negative_set:
		print('-' + word)
		return -10
	return 0

score = 0
print(tags)
for (word,pos) in tags:
	if pos[0:2] in ['NN', 'VB']:
		score += analyzeBase(word)


print(score)





