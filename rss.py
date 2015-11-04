from __future__ import division
from rss_config import negative_words, positive_words
import pull_rss
from analyze import Analyze

import os
import sys


POS_DIR = '/home/nick/repos/rss/moviedata/pos'
NEG_DIR = '/home/nick/repos/rss/moviedata/neg'

poslist = os.listdir(POS_DIR)
neglist = os.listdir(NEG_DIR)

negTrue = len(neglist)
negGuess = 0
for i in range(100):
	x = Analyze.fileSentiment(NEG_DIR + '/' + neglist[i])
	if x < 0:
		negGuess += 1


posTrue = len(poslist)
posGuess = 0
for i in range(100):
	x = Analyze.fileSentiment(POS_DIR + '/' + poslist[i])
	if x > 0:
		posGuess += 1

print(str(posGuess) + '/' + str(posTrue) + ' Correct on positive reviews')
cent = posGuess/posTrue
print(cent)

print(str(negGuess) + '/'+ str(negTrue) + ' Correct on negative reviews')
cent = negGuess/negTrue
print(cent)


while(1):
	text = input('Enter sentence:\n\r')
	text = Analyze.textSentiment(text)
	print(text)


# while(1):
# 	text = input('Enter sentence:\n\r')
# 	tokens = Analyze.textDetails(text)
# 	print(tokens)
	# for t in tokens:

