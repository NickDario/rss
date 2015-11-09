from __future__ import division
from rss_config import negative_words, positive_words
from pull_rss import RSS
from analyze import Analyze

import os
import sys
import sqlite3

RSS.pullStoriesToDB()

db = sqlite3.connect('rss.db')
c  = db.cursor()

stories = c.execute('SELECT id, title FROM stories WHERE sentiment IS NULL')

for id, title in stories:
	print(title, Analyze.textSentiment(title))


# POS_DIR = '/home/nick/repos/rss/moviedata/pos'
# NEG_DIR = '/home/nick/repos/rss/moviedata/neg'

# poslist = os.listdir(POS_DIR)
# neglist = os.listdir(NEG_DIR)

# x = 0
# while x < len(neglist):
# 	negTrue = len(neglist)
# 	negGuess = 0
# 	for i in range(x,x+100):
# 		v = Analyze.fileSentiment(NEG_DIR + '/' + neglist[i])
# 		if v < 0:
# 			negGuess += 1

# 	posTrue = len(poslist)
# 	posGuess = 0
# 	for i in range(x,x+100):
# 		v = Analyze.fileSentiment(POS_DIR + '/' + poslist[i])
# 		if v > 0:
# 			posGuess += 1

# 	print(str(x) + ' to ' + str((x+100)) + ':' + str(posGuess) + '/' + str(100) + ' Correct on positive reviews')
# 	cent = posGuess/100
# 	print(cent)
# 	print(str(x) + ' to ' + str((x+100)) + ':' + str(negGuess) + '/'+ str(100) + ' Correct on negative reviews')
# 	cent = negGuess/100
# 	print(cent)
# 	x += 100

# while(1):
# 	text = input('Enter sentence:\n\r')
# 	text = Analyze.textSentiment(text)
# 	print(text)



