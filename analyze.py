from nltk import word_tokenize
from nltk import pos_tag
import os
import sys

sys.path.append('/home/nick/repos/rss')

import rss_config

negative = open(SENTIMATE_DIR + '/negative-words.txt')
negative_set = [x.strip('\n') for x in negative.readlines()]

positive = open(SENTIMATE_DIR + '/positive-words.txt')
positive_set = [x.strip('\n') for x in positive.readlines()]

def analyzeBase(word):
	if word in positive_set:
		print('+' + word)
		return 10
	if word in negative_set:
		print('-' + word)
		return -10
	return 0

def analyzeTitle(title):
	tags = pos_tag(word_tokenize(title))
	score = 0
	for (word,pos) in tags:
		if pos[0:2] in ['NN', 'VB']:
			score += analyzeBase(word)
	return score

def sumSentimate():
	rss_list = os.listdir(RSS_LIST_DIR)
	feeds = {}
	for f in rss_list:
		info = f.split()
		if info[0] not in feeds:
			feeds[info[0]] = 0
		
		title = open(RSS_LIST_DIR + '/' + f).read()
		feeds[info[0]] += analyzeTitle(title)
	
	return feeds

print(sumSentimate())


